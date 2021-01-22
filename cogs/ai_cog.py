from discord.ext import commands
from config import ai_dir, ai_receptors


class AICog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        for receptor in ai_receptors:
            if receptor in message.content:
                try:
                    with open(f"{ai_dir}/ai_data.txt", "x"):
                        wr.write(f"{message.content}")
                except FileExistsError:
                    with open(f"{ai_dir}/ai_data.txt", "a") as wr:
                        wr.write(f"\n{message.content}")


def setup(bot):
    bot.add_cog(AICog(bot))
