#import 
import os,random as r
import discord
from discord.ext import commands

#local import
from lib import roles,channels


file= open(".token","r")
TOKEN=file.read()
bot = commands.Bot(command_prefix='!')



@bot.event
async def on_ready():
	print(f'Logged in as: {bot.user.name}')
	print(f'With ID: {bot.user.id}')

@bot.command()
async def rand(ctx):
	await ctx.send(r.randint(1,10))

@bot.command()
async def ping(ctx):
	await ctx.send("pong")

@bot.command()
@commands.is_owner()
async def testRoleExChan(ctx,args):
	msg= "creation d'un channel {}-no-mic visible uniquement du role {}".format(args,args)
	await ctx.send(msg)
	await channels.createRoleExclusiveChannel(ctx.guild,ctx.message.channel.category_id,args)

@bot.command()
@commands.is_owner()
async def SupRoleExChan(ctx,args):
	msg= "suppression du channel {}-no-mic et du role {}".format(args,args)
	await ctx.send(msg)
	await channels.suppressRoleExclusiveChannel(ctx.guild,ctx.message.channel.category_id,args)


@bot.command()
@commands.is_owner()
async def RoleCreate(ctx,args):
	msg= "creation du role {}".format(args)
	await ctx.send(msg)
	await roles.createRole(ctx.channel.guild, args)

@bot.command()
@commands.is_owner()
async def RoleSuppress(ctx,args):
	msg= "supression du role {}".format(args)
	await ctx.channel.send(msg)
	await roles.deleteRole(ctx.channel.guild,args)

@bot.command()
@commands.is_owner()
async def ChannelCreate(ctx,args):
	msg= "creation du channel {}".format(args)
	await ctx.channel.send(msg)
	await channels.createChannel(ctx.channel.guild,ctx.message.channel.category_id,args)
	
@bot.command()
@commands.is_owner()
async def ChannelSuppress(ctx,args):
	msg= "supression du channel {}".format(args)
	await ctx.channel.send(msg)
	await channels.deleteChannel(ctx.channel.guild, args)

@bot.command()
@commands.is_owner()
async def addRole(ctx,arg1,arg2):
	msg= "ajout du role {} a l'utilisateur {} ".format(arg2, arg1)
	member = ctx.guild.get_member_named(arg1)
	await ctx.channel.send(msg)
	await roles.addRoleToUser(ctx.channel.guild,member,arg2)


@bot.command()
@commands.is_owner()
async def removeRole(ctx,arg1,arg2):
	msg= "suppression du role {} a l'utilisateur {} ".format(arg2, arg1)
	await ctx.channel.send(msg)
	member = ctx.guild.get_member_named(arg1)
	await roles.removeRoleToUser(ctx.channel.guild,member,arg2)
	


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
				await channels.createRoleExclusiveChannel(after.channel.guild,after.channel.category_id,after.channel.name)

			await roles.addRoleToUser(after.channel.guild,member,after.channel.name)


	return 	



bot.run(TOKEN)
