import discord
import json
from discord.ext import commands
from helpers import build_link_list
from config import res_dir


class LinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def linki(self, ctx, message="all"):
        embed_var = discord.Embed(title=":shushing_face: Nieoficjalne linki:", description="semestr "+message,
                                  color=0xff770f)
        await build_link_list(ctx, embed_var, "linki", message)

    @commands.command()
    async def oflinki(self, ctx, message="all"):
        embed_var = discord.Embed(title=":mortar_board: Oficjalne linki:", color=0xff770f)
        await build_link_list(ctx, embed_var, "oflinki", message)

    @commands.command()
    async def link(self, ctx, *, comb):
        print(comb)
        subject = ""
        if len(comb.split(" ")) < 2:
            subject_alias = "".join(comb.split(" ")[1:])
            print(subject_alias)
            sem = comb.split(" ")[0]
            print(sem)
            with open(f"{res_dir}/subject_aliases.txt", "r") as rd:
                subject_alias_dict = json.loads(rd.read())[sem]
            for key in subject_alias_dict:
                if subject_alias in subject_alias_dict[key] or subject_alias == key:
                    subject = key
                    break
            print(subject_alias_dict[sem][subject])
            embed_var = discord.Embed(title=subject, description=subject_alias_dict[sem][subject], color=0xff770f)
            await ctx.send(embed=embed_var)
        else:
            await ctx.send("Za mało argumentów. Podaj komendę w postaci: !link <nr. semestru> <przedmiot>")


def setup(bot):
    bot.add_cog(LinkCog(bot))
