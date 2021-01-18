from discord.ext import commands
from dotenv import load_dotenv
import os
import youtube_dl
from helpers import *

load_dotenv()

# Set command prefix:
client = commands.Bot(command_prefix=prefix)

co_alias = read_lines(f'{res_dir}/co_aliases')
client.remove_command('help')
players = {}


@client.event
async def on_ready():
    print('Bot is ready.')


@client.event
async def on_guild_join(guild):
    await fetch_sv_data(guild)

# Commands:

@client.command(aliases=co_alias)
async def co(ctx, *, question=''):
    choice = get_random_number_unless_specified(question)
    await send_pic_or_txt_on_choice(ctx, choice)


@client.command()
async def load(ctx, extension):
    client.load_extension(f'{cogs_dir}.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'{cogs_dir}.{extension}')


# @client.command()
# async def clear(ctx, amount=5):
#     await ctx.channel.purge(limit=amount + 1)

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command()
async def sv(ctx):
    guild = ctx.message.guild
    await fetch_sv_data(guild)


@client.command()
async def secret(*, message):
    channel = client.get_channel(int(os.getenv("GENERAL")))
    embed_var = discord.Embed(title=f"{message}", color=0x00ff00)
    await channel.send(embed=embed_var)


@client.command()
async def help(ctx):
    embed_var = discord.Embed(title=":ledger: Komendy:", description=f"przed komenda dodaj \"{prefix}\"",
                              color=0xff770f)
    await build_link_list(ctx, embed_var)


if __name__ == '__main__':
    for filename in os.listdir(f'{cogs_dir}'):
        if filename.endswith('.py'):
            client.load_extension(f'{cogs_dir}.{filename[:-3]}')


client.run(os.getenv("DSC_BOT_KEY"))
