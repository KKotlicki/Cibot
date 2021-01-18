import discord
from discord.ext import commands
from helpers import open_help, build_link_list


class MainCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.command()
    async def thx(self, ctx):
        embed_var = discord.Embed(title=":evergreen_tree: Contributed to Cibot:", description="https://github.com"
                                                                                              "/KKotlicki/Cibot",
                                  color=0xff770f)
        await build_link_list(ctx, embed_var, "credits")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.client.latency * 1000)}ms')

    @commands.command()
    async def help(self, ctx):
        await open_help(ctx, "help")


def setup(client):
    client.add_cog(MainCog(client))
