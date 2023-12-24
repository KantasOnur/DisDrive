ATTACHMENT_SIZE = 25000000
TOKEN = 'MTE4ODIxMzIxMjM1MzY3OTQyMA.G6QnLC.ZIc7H2oHCmIoHv3bG0Kgf1yOruZ6L3IlC8RuYs'


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


def fileExists(con, fileName, size):
    cur = con.cursor()
    res = cur.execute(f"""SELECT * FROM files WHERE filename='{fileName}'""")
    if res.fetchone() is None:
        print("inserted")
        params = (fileName, size)
        cur.execute(f"""INSERT INTO files VALUES(?, ?, NULL, NULL)""", params)
        con.commit()
        return False

    return True

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

        if fileExists(con, fileName, size):
            await ctx.send("File already exists!")
            return

        numChunks = ceil(size / ATTACHMENT_SIZE)

        out = chunkifyFile(contents, fileName, size, numChunks)
        await ctx.send(fileName, files=out)

        for chunkNum in range(numChunks):
            os.remove(f"{fileName.split('.')[0]}_{chunkNum}.txt")

    client.run(TOKEN)


if __name__ == "__main__":
    import sqlite3
    import os
    import discord
    from discord.ext import commands
    from math import ceil
    main()
