import discord
import json
from discord.ext import commands
from helpers import build_link_list
from config import RES_PATH


class LinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def linki(self, ctx, message="all"):
        await ctx.channel.purge(limit=1)
        embed_var = discord.Embed(title=":shushing_face: Nieoficjalne linki:", description="semestr "+message,
                                  color=0xff770f)
        await build_link_list(ctx, embed_var, "linki", message)

    @commands.command()
    async def oflinki(self, ctx, message="all"):
        await ctx.channel.purge(limit=1)
        embed_var = discord.Embed(title=":mortar_board: Oficjalne linki:", color=0xff770f)
        await build_link_list(ctx, embed_var, "oflinki", message)

    @commands.command()
    async def link(self, ctx, sem, message):
        await ctx.channel.purge(limit=1)
        subject = ""
        with open(f"{RES_PATH}/subject_aliases.json", encoding='utf-8') as rd:
            subject_alias_dict = json.loads(rd.read())[sem]
        for key in subject_alias_dict:
            if message in subject_alias_dict[key] or message == key:
                subject = key
                break
        with open(f'{RES_PATH}/linki.json', encoding='utf-8') as rd:
            link = json.loads(rd.read())[sem][subject]
        embed_var = discord.Embed(title=subject, description=link, color=0xff770f)
        await ctx.send(embed=embed_var)


def setup(bot):
    bot.add_cog(LinkCog(bot))
