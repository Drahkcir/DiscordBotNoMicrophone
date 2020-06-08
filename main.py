#import 
import os,random as r
import discord
from discord.ext import commands

import logging

#local import
from lib import roles,channels

# logging configuration to get log in a file
logger = logging.getLogger('discord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#getting the token from the file ".token"
file= open(".token","r")
TOKEN=file.read()
bot = commands.Bot(command_prefix='$')



@bot.event
async def on_ready():
	print(f'Logged in as: {bot.user.name}')
	print(f'With ID: {bot.user.id}')

@bot.command()
@commands.is_owner()
async def ping(ctx):
	await ctx.send('latence : {0} ms'.format(round(bot.latency*1000,1)))

@bot.event
async def on_voice_state_update(member,before,after):
	print(str(member))
	if(before.channel != after.channel):
		if(before.channel != None):
			if(len(before.channel.members) == 0):
				print("last to quit the channel")			
				await channels.suppressRoleExclusiveChannel(before.channel.guild,before.channel.category_id,before.channel.name)
			else:
				await roles.removeRoleToUser(before.channel.guild,member,before.channel.name)
				print("quit the channel but their are still people in the channel")	
				
		if(after.channel != None):
			if(len(after.channel.members)== 1):
				print("first in the channel")
				await channels.createRoleExclusiveChannel(after.channel.guild,after.channel.category_id,after.channel.name,after.channel.position)

			await roles.addRoleToUser(after.channel.guild,member,after.channel.name)


	return 	



bot.run(TOKEN)
