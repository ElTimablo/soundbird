import discord
from discord.ext.commands import Bot
from discord import Intents
import random
import asyncio
import nacl
import time
import youtube_dl

intents=Intents.all()
random.seed(version=2)

bot = Bot(command_prefix='$')
token= "ODU3Mzc4ODc3MzAxODUwMTU0.YNOuTQ.UN6iy-4NtS17XErfS72Ble5Qu9M"
@bot.event
async def on_ready():
	print(f'{bot.user} in the house!')
	
@bot.command(name = 'test')
async def testFunc(context):
	print('Test received')
	await context.send('Is this thing on?')

# DEPRECATED
# @bot.command(name='dice', help='Rolls a die of the specified number of sides')
# async def rollDice(context, arg):
	# try:
		# r = random.randint(1, int(arg))
	# except ValueError:
		# await context.send("Enter an integer, dickhead")
	# else:
		# await context.send('You rolled ' + str(r))

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

# @bot.command(name='play')
# async def play(context, channel: discord.VoiceChannel = None, ):
	# voice_channel = context.author.voice.channel
	# if voice_channel != None:
		# channel = voice_channel.name
		# vc = await voice_channel.connect()
		
		# vc.play(discord.FFmpegPCMAudio(
		
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
			send_str = "You rolled "+ str(dice[0]) + "d" + str(dice[1]) + part[1] + part[2] + " " + (str(dlist) if len(dlist) > 1 or addsub != 0 else "") + ", getting " + str(total)
			if len(send_str) < 2001:
				await context.send(send_str)
			else:
				await context.send("You rolled a shitload of dice, getting "+ str(total) + ".")

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

bot.run(token)
