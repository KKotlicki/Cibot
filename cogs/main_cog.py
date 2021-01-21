import discord
from discord.ext import commands
from helpers import open_help, build_link_list


class MainCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')

    @commands.command()
    async def thx(self, ctx):
        embed_var = discord.Embed(title=":evergreen_tree: Contributed to Cibot:", description="https://github.com"
                                                                                              "/KKotlicki/Cibot",
                                  color=0xff770f)
        await build_link_list(ctx, embed_var, "credits")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def help(self, ctx):
        await open_help(ctx, "help")

    @commands.command()
    async def bug(self, ctx, message):
        user = self.bot.get_user(516640010129375234)
        author = message.author
        await user.send(message + '\n\n<' + author + '>')


def setup(bot):
    bot.add_cog(MainCog(bot))
