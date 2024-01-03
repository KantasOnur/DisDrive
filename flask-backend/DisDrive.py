from urllib.request import urlopen, Request
import sqlite3
import os
import json
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

ATTACHMENT_SIZE = 25000000

client = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@client.event
async def on_ready():
    print("The bot is ready to use!")
    checkForRequests.start()


def waitForServer():
    while not os.path.exists('message.json'):
        continue


async def upload(request):
    con = sqlite3.connect("files.db")
    cur = con.cursor()

    for chunkid in range(request['totalchunks']):
        waitForServer()
        chunkfile = f"{request['filename'].split('.')[0]}_{chunkid}.txt"
        message = await client.get_channel(CHANNEL_ID).send(file=discord.File(chunkfile))
        cur.execute(f"INSERT INTO files VALUES(?, ?, ?, ?)",
                    [request['filename'], request['size'], message.id, chunkid])
        os.remove(chunkfile)
        os.remove('message.json')  # once removed server no longer waits for bot

    con.commit()
    con.close()


async def download(filename):
    con = sqlite3.connect("files.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT messageid FROM files WHERE filename=? ORDER BY chunkid ASC",
                      [filename])


    with open(filename, "ab") as download_file:
        for tuple in res.fetchall():
            message = await client.get_channel(CHANNEL_ID).fetch_message(tuple[0])
            url = message.attachments[0].url
            req = Request(url=str(url),
                          headers={'User-Agent': 'Mozilla/5.0'})
            content = urlopen(req).read()
            download_file.write(content)

    con.commit()
    con.close()


async def delete(filename):
    con = sqlite3.connect("files.db")
    cur = con.cursor()

    res = cur.execute(f"SELECT messageid FROM files WHERE filename=? ORDER BY chunkid ASC",
                      [filename])
    con.commit()

    for tuple in res.fetchall():
        message = await client.get_channel(CHANNEL_ID).fetch_message(tuple[0])
        await message.delete()

    cur.execute(f"DELETE FROM files WHERE filename=?", [filename])
    con.commit()
    con.close()


@tasks.loop(seconds=1)
async def checkForRequests():
    if os.path.exists('message.json'):
        with open('message.json', 'r') as file:
            request = json.load(file)

        if request['requestType'] == 'upload':
            await upload(request)

        if request['requestType'] == 'download':
            await download(request['filename'])
            os.remove("message.json")

        if request['requestType'] == 'delete':
            await delete(request['filename'])
            os.remove('message.json')


client.run(TOKEN)
