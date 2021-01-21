import discord
from discord.ext import commands
from helpers import build_link_list


class LinkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def linki(self, ctx, message):
        embed_var = discord.Embed(title=":shushing_face: Nieoficjalne linki:", description="semestr "+message,
                                  color=0xff770f)
        await build_link_list(ctx, embed_var, "linki", message)

    @commands.command()
    async def oflinki(self, ctx, message="all"):
        embed_var = discord.Embed(title=":mortar_board: Oficjalne linki:", color=0xff770f)
        await build_link_list(ctx, embed_var, "oflinki", message)

    # @commands.command()
    # async def link(self, ctx, *, comb):
    #     subject = ""
    #     with open(f"{res_dir}/subject_aliases.txt", "r") as rd:
    #         subject_alias_dict = json.loads('{' + rd.read() + '}')
    #     for key in subject_alias_dict:
    #         if subject_alias in subject_alias_dict[key] or subject_alias == key:
    #             subject = key
    #             break
    #     help_json = "".join(read_lines(f'{res_dir}/linki'))
    #     embed_var = discord.Embed(title=subject, description=json.loads('{' + help_json + '}')[subject], color=0xff770f)
    #     await ctx.send(embed=embed_var)


def setup(bot):
    bot.add_cog(LinkCog(bot))
