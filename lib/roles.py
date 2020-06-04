import discord

async def createRole(guild,roleName):
    role = await guild.create_role(name=roleName)
    print("Role {} créer".format(roleName))
    return role


async def deleteRole(guild,roleName):
    role = discord.utils.get(guild.roles, name=roleName)
    if role:
        await role.delete()
        print("Role {} supprime ".format(roleName) )
    else:
        print("Role non trouve")


async def addRoleToUser(guild,member:discord.Member ,roleName):
    role = discord.utils.get(guild.roles, name=roleName)   
    await member.add_roles(role)
    print("user {} added to the role {}".format(member,role))



async def removeRoleToUser(guild,member:discord.Member ,roleName):
    role = discord.utils.get(guild.roles, name=roleName)   
    await member.remove_roles(role)
    print("user {} added to the role {}".format(member,role))