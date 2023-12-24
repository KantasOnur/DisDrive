ATTACHMENT_SIZE = 25000000
TOKEN = 'MTE4ODIxMzIxMjM1MzY3OTQyMA.GHHpwM.s_2Fm9ND0vDpdFuGtRD2WW6GHEEsr9gpfu2TCQ'


def readFile(path):
    with open(path, "rb") as f:
        contents = f.read()
    f.close()
    return contents


def writeChunkFile(fileName, chunkNum, chunkContents):
    chunkFile = f"{fileName.split('.')[0]}_{chunkNum}.txt"
    with open(chunkFile, "wb") as outF:
        outF.write(chunkContents)

    return chunkFile


def chunkifyFile(contents, fileName, size, numFiles):
    firstByte = 0
    lastByte = size  # either 25k or end of file
    filesToSend = []

    if size > ATTACHMENT_SIZE:
        lastByte = ATTACHMENT_SIZE

    for chunkNum in range(numFiles):

        chunkContents = contents[firstByte:lastByte]
        contents = contents[lastByte:size]  # slice the recently read bytes
        chunkFile = writeChunkFile(fileName, chunkNum, chunkContents)

        with open(chunkFile, "rb") as file:
            filesToSend.append(discord.File(file))

        lastByte = size - lastByte  # either add 25k or end of file
        if lastByte > ATTACHMENT_SIZE:
            lastByte = ATTACHMENT_SIZE

    return filesToSend


def insertToDb(con, fileName, size):
    cur = con.cursor()
    print("inserted")
    params = (fileName, size)
    cur.execute(f"INSERT INTO files VALUES(?, ?, NULL, NULL)", params)
    con.commit()


def fileExists(cur, fileName):
    res = cur.execute(f"SELECT * FROM files WHERE filename='{fileName}'")
    if res.fetchone() is None:
        return False
    return True

def insertMessageId(con,cur,message,fileName):
    cur.execute(f"""UPDATE files SET messageid = ? WHERE filename = ?""", (message.id, fileName))
    con.commit()

def main():
    client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    con = sqlite3.connect("files.db")
    cur = con.cursor()

    @client.event
    async def on_ready():
        print("The bot is ready to use!")

    @client.command(pass_context=True)
    async def upload(ctx, path):
        fileName = path.split('/')[-1]
        contents = readFile(path)
        size = len(contents)

        if fileExists(con, fileName):
            await ctx.send("File already exists!")
            return

        insertToDb(con, fileName, size)
        numChunks = ceil(size / ATTACHMENT_SIZE)

        out = chunkifyFile(contents, fileName, size, numChunks)
        await ctx.send(f"UPLOADING {fileName} DO NOT EXECUTE ANY OTHER COMMAND!")
        message = await ctx.send(fileName, files=out)
        insertMessageId(con, cur, message, fileName)

        for chunkNum in range(numChunks):
            os.remove(f"{fileName.split('.')[0]}_{chunkNum}.txt")  # clean-up the chunk files

    @client.command(pass_context=True)
    async def download(ctx, fileName, size):

        if fileExists(cur, fileName):
            res = cur.execute(f"SELECT messageid FROM files WHERE filename=?", [fileName])
            messageid = res.fetchone()[0]
            message = await ctx.fetch_message(messageid)
            print(message.attachments[0])



    client.run(TOKEN)


if __name__ == "__main__":
    import sqlite3
    import os
    import discord
    from discord.ext import commands
    from math import ceil
    main()
