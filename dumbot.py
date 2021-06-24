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

@bot.command(name='dice', help='Rolls a die of the specified number of sides')
async def rollDice(context, arg):
	try:
		r = random.randint(0, int(arg))
	except ValueError:
		await context.send("Enter an integer, dickhead")
	else:
		await context.send('You rolled ' + str(r))

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
bot.run(token)
