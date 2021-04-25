from concurrent.futures import ThreadPoolExecutor
import os
from googleapiclient.discovery import MediaFileUpload
import requests
from discord.ext import commands, tasks
import discord
from datetime import datetime
from utils.drive_oauth import service
import json
from config import SV_PATH, TEMP_PATH, LOGS_PATH
from loguru import logger
from helpers import set_sv_config, get_text_channel_id_from_name


class DriveCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api = service
        self.is_running = False
        self.check_for_drive_updates.start()

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
            with open(f'{SV_PATH}/{ctx.guild.name}_drive_ids.json', encoding='utf-8') as rd:
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
                folder_id = directories_dict[message][0]
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

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(pass_context=True, aliases=['set_google', 'set_drv', 'set_disc'])
    @commands.has_permissions(administrator=True)
    async def set_drive(self, ctx, *, message=''):
        if message == '':
            message = ctx.channel.name
        try:
            get_text_channel_id_from_name(ctx.guild.name, message)
        except KeyError:
            await ctx.send("Nie znam takiego kanału.")
        else:
            await ctx.channel.purge(limit=1)
            await set_sv_config(ctx, message, 'drive')
            logger.success(f"@{ctx.author.name} in {ctx.guild.name} set drive channel to #{message}")
            await ctx.send(f"✅ Kanał na aktualizacje dysku ustawiony na #{message}")

    @tasks.loop(minutes=5)
    async def check_for_drive_updates(self):
        for fn in os.listdir(f"{SV_PATH}/"):
            if fn.endswith("_drive_ids.json"):
                with open(f"{SV_PATH}/{fn}") as rd:
                    folder_dict = json.loads(rd.read())
                for folder_name, folder_id in folder_dict.items():
                    if len(folder_id) == 2:
                        if not os.path.isfile(f"{TEMP_PATH}/{folder_id[0]}.txt"):
                            item_list = get_drive_folder_file_names(folder_id)
                            with open(f"{TEMP_PATH}/{folder_id[0]}.txt", "w+") as wr:
                                wr.writelines(item_list)
                        else:
                            with open(f"{TEMP_PATH}/{folder_id[0]}.txt") as rd:
                                old_items = rd.readlines()
                            item_list = get_drive_folder_file_names(folder_id)
                            if list(set(item_list) - set(old_items)):
                                with open(f"{TEMP_PATH}/{folder_id[0]}.txt", "w") as wr:
                                    wr.writelines(item_list)
                                for guild in self.bot.guilds:
                                    if guild.name == fn[:-15]:
                                        with open(f"{SV_PATH}/{fn[:-15]}_config.json") as rd:
                                            config = json.loads(rd.read())
                                        for channel in guild.channels:
                                            if channel.name == config["drive"]:
                                                list_of_new_files = ""
                                                for new_file in list(set(item_list) - set(old_items)):
                                                    list_of_new_files += f"\n{new_file[:-38]}"
                                                embed = discord.Embed(title=f"Na dysku w folderze *{folder_name}* "
                                                                            f"pojawiły się nowe pliki:",
                                                                      description=list_of_new_files,
                                                                      color=discord.Color.orange())
                                                await channel.send(embed=embed)


def get_drive_folder_file_names(folder_id: list):
    results = service.files().list(q=f"'{folder_id[0]}' in parents", pageSize=100,
                                   fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    item_list = []
    for item in items:
        item_list.append(f"{item['name']} - {item['id']}\n")
    return item_list


def upload_file(metadata, media):
    return service.files().create(body=metadata, media_body=media).execute()


def setup(bot):
    bot.add_cog(DriveCog(bot))
