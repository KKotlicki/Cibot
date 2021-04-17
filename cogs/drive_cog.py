from concurrent.futures import ThreadPoolExecutor
import os
from googleapiclient.discovery import MediaFileUpload
import requests
from discord.ext import commands
import discord
from datetime import datetime
from utils.drive_oauth import service
import json
from config import SV_PATH, TEMP_PATH, LOGS_PATH


class DriveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = service
        self.is_running = False

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['contributions', 'hall_of_fame', 'hall'])
    async def contr(self, ctx):
        await ctx.channel.purge(limit=1)
        ranking = {}
        with open(f'{LOGS_PATH}/upload_history.log', encoding='utf-8') as rd:
            upload_history = rd.readlines()
        for line in upload_history:
            parsed_line = line[:-1].split(' | ')
            if parsed_line[4] == 'open':
                if parsed_line[1][:-5] in ranking:
                    ranking[parsed_line[1][:-5]] += 1
                else:
                    ranking.update({parsed_line[1][:-5]: 1})
        temp = 1
        contributor_list = ''
        for key, value in ranking.items():
            if temp == 1:
                contributor_list += f'👑  **{key}** - **`{value}`**\n'
            else:
                contributor_list += f'\n{temp}. {key} - `{value}`'
            temp += 1
        embed = discord.Embed(title='Ranking kontrybutorów dysku:',
                              description=contributor_list, color=discord.Color.gold())
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['upl', 'send', 'drive'])
    async def upload(self, ctx, message):
        await self.upload_command(ctx, message, 'open')

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['ann_upload', 'annonymous_upload', 'hidden_upload', 'hidupl', 'hiddrive'])
    async def anupl(self, ctx, message):
        await self.upload_command(ctx, message, 'hidden')

    async def upload_command(self, ctx, message, is_hidden):
        await ctx.channel.purge(limit=1)
        if self.is_running:
            await ctx.send('Poczekaj aż skończę wysyłać pliki')
            return
        if message == '.gitkeep':
            await ctx.send('Nieprawidłowa nazwa pliku')
            return
        try:
            for fn in os.listdir(f'{TEMP_PATH}/drive_cache/'):
                if fn != ".gitkeep":
                    os.remove(f'{TEMP_PATH}/drive_cache/{fn}')
        except PermissionError:
            ctx.send("Poczekaj aż skończę wysyłać pliki")
        else:
            if not ctx.message.attachments:
                await ctx.send('Załącz do komendy plik do wysłania')
                return
            message = str(message).upper()
            if message in ['M', 'MAG', 'MAGISTERSKIE', 'MASTERS', 'MGR']:
                message = 'MASTERS'
            with open(f'{SV_PATH}/drive_ids.json', encoding='utf-8') as rd:
                directories_dict = json.loads(rd.read())
            attachment = ctx.message.attachments[0]
            if message not in directories_dict:
                temp_string = "**Wybierz semestr z listy:**\n"
                for key in directories_dict:
                    if key != "MASTERS":
                        temp_string += f" {key},"
                    else:
                        temp_string += f" Mgr"
                await ctx.send(temp_string)
                return

            async with ctx.typing():
                self.is_running = True
                folder_id = directories_dict[message]
                attachment_url = attachment.url
                file_request = requests.get(attachment_url)
                with open(f'{LOGS_PATH}/upload_history.log', 'a+') as wr:
                    wr.write(f'{datetime.now()} | {ctx.author} | '
                             f'{attachment.filename} | {message} | {is_hidden}\n')
                with open(f'{TEMP_PATH}/drive_cache/{attachment.filename}', "wb") as file:
                    file.write(file_request.content)
                metadata = {'name': attachment.filename, 'mimetype': attachment.content_type,
                            'parents': [folder_id]}
                media = MediaFileUpload(f'{TEMP_PATH}/drive_cache/{attachment.filename}',
                                        mimetype=attachment.content_type, resumable=True)
                with ThreadPoolExecutor() as pool:
                    await self.bot.loop.run_in_executor(pool, upload_file, metadata, media)
            if is_hidden == "open":
                embed = discord.Embed(title=f"🎉 Nowe materiały!",
                                      description=f"{ctx.author.mention} wysłał na dysk grupy semestralnej "
                                                  f"**{message}**:\n***{attachment.filename}***",
                                      color=discord.Color.gold())
                await ctx.send(embed=embed)
            for fn in os.listdir(f'{TEMP_PATH}/drive_cache/'):
                if fn != ".gitkeep":
                    try:
                        os.remove(f'{TEMP_PATH}/drive_cache/{fn}')
                    except PermissionError:
                        pass
            self.is_running = False


def upload_file(metadata, media):
    return service.files().create(body=metadata, media_body=media).execute()


def setup(bot):
    bot.add_cog(DriveCog(bot))
