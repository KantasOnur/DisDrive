ATTACHMENT_SIZE = 25000000
TOKEN = 'MTE4ODIxMzIxMjM1MzY3OTQyMA.GDweNz.xhc3UxgjiNHGG3isto9bfvdfT7UUNypJ8_leGY'

def readFile():
    with open(sys.argv[1], "rb") as f:
        contents = f.read()
    f.close()
    return contents

def writeChunkFile(fileName, chunkNum, chunkContents):
    chunkFile = f"output/{fileName.split('.')[0]}_{chunkNum}.txt"
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
        contents = contents[lastByte:size]
        chunkFile = writeChunkFile(fileName, chunkNum, chunkContents)

        with open(chunkFile, "rb") as file:
            filesToSend.append(discord.File(file))

        lastByte = size - lastByte  # either add 25k or end of file
        if lastByte > ATTACHMENT_SIZE:
            lastByte = ATTACHMENT_SIZE

    return filesToSend

def main():

    contents = readFile()

    fileName = sys.argv[1].split('/')[-1]
    size = len(contents)
    numFiles = ceil(size / ATTACHMENT_SIZE)

    out = chunkifyFile(contents, fileName, size, numFiles)

    # client = commands.Bot(command_prefix = '!', intents=discord.Intents.all())

    # @client.event
    # async def on_ready():
    #     print("The bot is ready to use!")
    #
    # @client.command(pass_context = True)
    # async def hello(ctx):
    #     await ctx.send(files=out)
    #
    # client.run(TOKEN)

if __name__ == "__main__":
    import discord
    from discord.ext import commands
    from math import ceil
    import sys

    main()
