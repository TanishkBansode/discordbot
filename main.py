import discord
from discord.ext import commands
from discord import app_commands
from typing import Tuple
from typing import List
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print("Bot Ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print("error")
"""@bot.command()
async def test(ctx, *args):
    arguments = ', '.join(args)
    await ctx.send(f'{len(args)} arguments: {arguments}')"""

import random

class Slapper(commands.Converter):
    async def convert(self, ctx, argument):
        to_slap = random.choice(ctx.guild.members)
        return f'{ctx.author} slapped {to_slap} because *{argument}*'

"""class JoinDistance:
    def __init__(self, joined, created):
        self.joined = joined
        self.created = created

    @property
    def delta(self):
        return self.joined - self.created

class JoinDistanceConverter(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return JoinDistance(member.joined_at, member.created_at)

@bot.command()
async def delta(ctx, *, member: JoinDistanceConverter):
    is_new = member.delta.days < 100
    if is_new:
        await ctx.send(f"Hey you're pretty new!: {member.delta.days} days")
    else:
        await ctx.send(f"Hm you're not so new.: {member.delta.days} days")"""
        

import typing

@bot.command()
async def union(ctx, what: typing.Union[discord.TextChannel, discord.Member]):
    await ctx.send(what)

@bot.command()
async def objekt(ctx, amount: typing.Optional[int] = 1, *, objects="beer"):
    await ctx.send(f'{amount} {objects} on the wall!')
    
from typing import Literal

@bot.tree.command(name="shop")
async def shop(interaction:discord.Interaction, buy_sell: Literal['buy', 'sell'], amount: Literal[1, 2], *, item: str):
    await interaction.response.send_message(f'{buy_sell.capitalize()}ing {amount} {item}(s)!')

from typing import Annotated

@bot.command()
async def fun(ctx, arg: Annotated[str, lambda s: s.upper()]):
    await ctx.send(arg)


@bot.tree.command(name="joined")
async def joined(interaction:discord.Interaction, *, member: discord.Member):
    await interaction.response.send_message(f'{member} joined on {member.joined_at}')

@bot.command()
async def delete(ctx, *, arg):
    await ctx.message.delete(delay=None)
    await ctx.send(arg)

@bot.command()
async def upload(ctx, attachment: typing.Optional[discord.Attachment]):
    if attachment is None:
        await ctx.send('You did not upload anything!')
    else:
        await ctx.send(f'You have uploaded <{attachment.url}>')


class BanFlags(commands.FlagConverter):
    question: str
    answer: str
    

@bot.tree.command(name='ask')
async def ask(interaction:discord.Interaction, *,question: str, answer: str):
    await interaction.response.send_message(f'''**Question**:{question}
**Answer**: {answer}''')




class BanFlags(commands.FlagConverter):
    members: Tuple[discord.Member, ...]
    reason: str

@bot.command()
async def smash(ctx, *, flags: BanFlags):
    for member in flags.members:
        print(member)
    members = ', '.join(str(member) for member in flags.members)
    await ctx.send(f'Smashed {members} for {flags.reason!r}')


class Coordinates(commands.FlagConverter):
    to: Tuple[int, int, int]
    
@bot.command()
async def travel(ctx, *, flags:Coordinates):
    await ctx.send(f'{ctx.author} travelled to {flags.to}')
@bot.command()
async def clean(ctx, *, content: commands.clean_content):
    await ctx.send(content)

def to_upper(argument):
    return argument.upper()

async def clean(ctx, *, content: commands.clean_content(use_nicknames=False)):
    await ctx.send(content)

@bot.command()
async def up(ctx, *, content: to_upper):
    await ctx.send(content)

@bot.command()
async def yesorno(ctx, *, arg):
    if arg.lower() in ('yes', 'y', 'true', 't', '1', 'enable', 'on'):
        await ctx.send("ok")
    elif arg.lower() in ('no', 'n', 'false', 'f', '0', 'disable', 'off'):
        await ctx.send("not ok")
    if arg == "Am i smart?":
        await ctx.send("Yes ofc")
    elif arg == "Am i dumb?":
        await ctx.send("Don't say that ")
    await ctx.send(f"{ctx.guild}:{ctx.author}: {ctx.message}")
   
@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a + b)



bot.run('key')
