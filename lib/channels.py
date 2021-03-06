import discord,re
import lib.roles



async def createChannel(guild,categoryId,name,position):
    category = discord.utils.get(guild.channels, id=categoryId)
    channel = await guild.create_text_channel(name=name,category=category,position=position)
    print("channel {} creer".format(name))
    return channel

async def deleteChannel(guild,name):
    channel = discord.utils.get(guild.channels, name=name)
    if channel:
        await channel.delete()
        print("channel {} supprime".format(name))
    else:
        print("channel {} non trouve".format(name))

async def createRoleExclusiveChannel(guild,categoryId,name,position):
    chanName="{}-no-micro".format(name)
    role = await lib.roles.createRole(guild,name)
    discord.utils.get(guild.roles, name=name)
    category = discord.utils.get(guild.channels, id=categoryId)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me : discord.PermissionOverwrite(read_messages=True),
        role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(name=chanName,category=category, overwrites=overwrites)
    await channel.edit(position=int(position)) 
    
async def suppressRoleExclusiveChannel(guild,categoryId,name):
    role = discord.utils.get(guild.roles, name=name)
    chanName=name.lower()
    chanName = re.sub(r'\s+', '-', chanName) 
    print("chanName : {}".format(chanName))
    chanName="{}-no-micro".format(chanName)
    await deleteChannel(guild,chanName)
    await lib.roles.deleteRole(guild,name)
