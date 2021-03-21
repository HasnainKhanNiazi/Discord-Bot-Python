import discord
from discord.ext import commands
import random
import datetime
import asyncio

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)

# client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there!'))
    print('Bot is ready.')

@client.command()
async def guild_ID(ctx):
    guild_id = ctx.guild.id
    await ctx.send(guild_id)

@client.command()
async def gstart(ctx, mins: int, *, prize: str):
    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = mins*60)
    embed.add_field(name="Ends At:", value=f"{end} UTC")
    embed.set_footer(text=f"Ends {mins} minutes from now!")
    my_msg = await ctx.send(embed = embed)
    await my_msg.add_reaction("🎉")
    await asyncio.sleep(mins * 60)
    new_msg = await ctx.channel.fetch_message(my_msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)
    await ctx.send(f"Congratulations {winner.mention} won {prize}!")

@client.event
@commands.has_permissions(manage_roles = True)
async def on_member_join(member):
    print(f'{member} has joined the server.')
    em = discord.Embed(title="Custom Fiverr Bot", description=f"Welcome to our custom fiverr bot server, Please welcome {member.mention} to our server!")
    await member.send(embed=em)
    guild = member.guild
    mute_role = discord.utils.get(member.guild.roles, name = "Muted")
    await guild.create_role(name = "Muted", color = discord.Color(0x000001))
    await member.send("Created Role")
    await member.add_roles(mute_role)
    await member.send("Muted")

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}')

@client.command()
async def dio(ctx):
    await ctx.send('Porco')

@client.command()
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'Banned {member.mention}')

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return

@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, Question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    
    await ctx.send(f'Question: {Question}\nAnswer: {random.choice(responses)}')

client.run('ODIyNDc0ODMyMTI2MDE3NTg5.YFSzYA.MQ8e5Dr1Sg4jax80UllBMEKDuso')