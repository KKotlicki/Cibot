from discord.ext import commands
from config import ai_dir, ai_receptors


class AICog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    @commands.Cog.listener()
    async def on_message(self, message):
        for receptor in ai_receptors:
            if receptor in message.content:
                with open(f"{ai_dir}/ai_data.txt", "r") as rd:
                    temp = rd.read()
                with open(f"{ai_dir}/ai_data.txt", "w+") as wr:
                    wr.write(f"{temp}\n => \n{message.content}")


def setup(client):
    client.add_cog(AICog(client))
