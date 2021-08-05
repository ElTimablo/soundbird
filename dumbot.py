import discord
from discord.ext.commands import Bot
from discord import Intents
import random
import asyncio
import nacl
import time
import youtube_dl
import mariadb
import sys
import os
import requests


storagepath = './'
intents=Intents.all()
random.seed(version=2)
penis_size = 1
bot = Bot(command_prefix='$')

# These must be set on the command line or through Docker or else the bot won't start
token = os.environ['DISCORD_TOKEN']
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASS']
db_host = os.environ['DB_HOST']
db_port = os.environ['DB_PORT']
db_database = os.environ['DB_DATABASE']


def connectDB():
    try:
        conn = mariadb.connect(user = db_user, password = db_password, host = db_host, port = int(db_port), database = db_database)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        sys.exit(1)
    return conn


@bot.event
async def on_ready():
        print(f'{bot.user} in the house!')


@bot.command(name = 'test')
async def testFunc(context):
        print('Test received')
        await context.send('Is this thing on?')


# Join the specified voice channel, or the author's if none is specified
@bot.command(name='connect', help='Connect the bot to a voice channel.')
async def vc_connect(context, *, channel: discord.VoiceChannel = None):
        dest = channel if channel else context.author.voice.channel
        if context.voice_client:
                await context.voice_client.move_to(dest)
                await context.send("Joined " + dest.name)
        else:
                await dest.connect()
                await context.send("Joined " + dest.name)


# Leave current voice channel
@bot.command(name='disconnect', help='Drop everything and leave voice')
async def vc_disconnect(context):
        await context.voice_client.disconnect()


# Goose
@bot.command(name='honk')
async def honk(context, channel: discord.VoiceChannel = None):
        voice_channel = context.author.voice.channel
        if voice_channel != None:
                channel = voice_channel.name
                vc = await voice_channel.connect()
                vc.play(discord.FFmpegPCMAudio(source="goose.mp3"))
                while vc.is_playing():
                        time.sleep(.1)
                await vc.disconnect()
        else:
                await context.send(str(context.author.name) + " is not in a channel.")
        await context.message.delete()


@bot.command(name='roll', help='Specify the size and number of dice to roll (5d6, 10d8, 1d20). Without context, will roll 1d20.')
async def roll_dice(context, arg="1d20"):
        arg = arg.lower()
        part = get_mod(arg)
        arg = part[0]
        try:
                mod = int(part[2]) if part[2] != "" else 0
        except ValueError:
                await context.send("You fucked up... try again.")
        else:
                addsub = 1 if part[1] == "+" else -1 if part[1] == "-" else 0

                try:
                        dice = cut_into_ints(arg)
                        total = mod * addsub
                        dlist = []
                        for i in range(dice[0]):
                                roll = random.randint(1, dice[1])
                                dlist.append(roll)
                                total += roll
                except ValueError:
                        await context.send("Enter an integer, dickhead")
                else:
                        send_str = f"You rolled {dice[0]}d{dice[1]}{part[1]}{part[2]} "+ (str(dlist) if len(dlist) > 1 or addsub != 0 else "") + f", getting {total}."
                        if len(send_str) < 2001:
                                await context.send(send_str)
                        else:
                                await context.send(f"You rolled a shitload of dice, getting {total}.")


def get_mod(arg: str) -> tuple:

        if "+" in arg:
                return arg.partition("+")
        elif "-" in arg:
                return arg.partition("-")
        else:
                return (arg, "", "")


def cut_into_ints(arg: str) -> tuple:
        if "d" in arg:
                part = arg.partition("d")
                return (int(part[0] if part[0] != "" else "1"), int(part[2]))
        else:
                return (1, int(arg))


@bot.command(name="penis", help="Be the biggest dick you can be")
async def penis(context):
        conn = connectDB()
        cur = conn.cursor()
        user = context.author
        penis_size = 1
        cur.execute("SELECT penus FROM users WHERE name like %s", (str(user),))
        penis_size = cur.fetchall()

        # New users will return an empty list. In this case, set penis_size to 1
        if penis_size == []:
            penis_size=1
        else:
        # Fetchall returns a list of tuples. fetchone() is probably what I actually want here, but so fucking what
            penis_size = penis_size[0][0]
        cur.execute("INSERT INTO users (name, penus) VALUES (?, ?) ON DUPLICATE KEY UPDATE penus=?", (str(user), penis_size+1, penis_size+1) )
        # Just in case the host has autocommit turned off by default
        conn.commit()
        shaft = ""
        for i in range(penis_size):
                shaft = shaft + "="
        await context.send(f"{context.author.mention} ((_){shaft}D")

        penis_size += 1 if penis_size < 1995 else 0
        await context.message.delete()
        conn.close()


@bot.command(name="dickstats", help="See who's got the biggest willy")
async def dickstats(context):
    user = context.author
    conn = connectDB()
    cur = conn.cursor()
    cur.execute("SELECT name, penus FROM users ORDER BY penus DESC;")
    topDicks = cur.fetchall()
    sendstring = "``"
    col_width = 30
    for name,peen in topDicks:
        sendstring = sendstring + str(name).ljust(col_width) + "\t\t\t" + str(peen).rjust(5) + "\n"
    sendstring = sendstring + "``"
    await context.send(f"{sendstring}")


@bot.command(name="slurp", help="Upload a file if you have permission")
async def slurp(context):
    conn = connectDB()
    cur = conn.cursor()
    user = context.author
    cur.execute("SELECT admin FROM users WHERE name LIKE %s", (str(user),))
    isAdmin = cur.fetchall()
    attachmentList = ""
    if isAdmin:
        for attachment in context.message.attachments:
            attachmentList += attachment.url + " "
            upload = requests.get(attachment.url)
            open(storagepath + attachment.filename, 'wb').write(upload.content)
        if attachmentList != "":
           await context.send(attachmentList)
        else:
            await context.send("Nothing")
    else:
        await context.send("Fuggoff")
    conn.close()

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

@bot.command(name='play')
async def play(context, arg, channel: discord.VoiceChannel = None):
    voice_channel = ""
    if context.author.voice != None:
        voice_channel = context.author.voice.channel
    filelocation = find(arg + ".mp3", storagepath)
    print("file: ", filelocation)
    if filelocation == None:
        await context.send("Sound clip not found")
        return
    print(voice_channel)
    if voice_channel:
        channel = voice_channel.name
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(source=filelocation))
        while vc.is_playing():
            time.sleep(.1)
        await vc.disconnect()
    else:
        await context.send(str(context.author.name) + " is not in a channel.")
    await context.message.delete()
bot.run(token)
