from discord.ext import commands, tasks
import os


class RaspberryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(minutes=5.0)
    async def rasp_temp(self):
        temp = os.popen("vcgencmd measure_temp").readline()
        print(temp)
        if float(temp.replace("temp=", "").replace("'C", "")) > 59.0:
            await self.bot.close()


def setup(bot):
    bot.add_cog(RaspberryCog(bot))
