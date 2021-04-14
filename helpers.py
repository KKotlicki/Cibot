import random
import discord
from config import *
from termcolor import colored
import glob
import json
import youtube_dl
import asyncio
import os


def read_lines(fname):
    with open(f"{fname}.txt", encoding='utf-8') as rs:
        return rs.read().splitlines()


async def open_help(ctx, file_name):
    is_admin = ""
    if file_name == "adm_help":
        is_admin = " dla Moderatorów"
    embed_var = discord.Embed(title=f"📒 **Lista Komend{is_admin}**:", color=0xff770f)
    embed_var.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/c/c8/WEL_WAT.jpg")
    with open(f'{RES_PATH}/{file_name}.json', encoding='utf-8') as rd:
        help_json = json.loads(rd.read())
    for name, value in help_json.items():
        command_list = ""
        for name1, value1 in value.items():
            command_list += f'`{PREFIX}{value1}` - {name1}\n'
        embed_var.add_field(name=f"\u200b\n{name}", value=command_list, inline=False)
    embed_var.set_footer(text="Komendy mają też nazwy zastępcze. "
                              "Jeśli chcesz dodać nazwę zastępczą lub stworzyć nową komendę, "
                              "zmień kod w repo lub skontaktuj się z deweloperami.")
    await ctx.send(embed=embed_var)


async def fetch_sv_data(ctx):
    text_names = []
    voice_names = []
    for channel in ctx.guild.text_channels:
        text_names.append(f'{str(channel)} => {channel.id}')
    for channel in ctx.guild.voice_channels:
        voice_names.append(f'{str(channel)} => {channel.id}')
    with open(f"{SV_PATH}/{ctx.guild}.json", "w+") as fn:
        fn.write(json.dumps({"text": text_names, "voice": voice_names}))
    await ctx.send("Zapisałem pomyślnie")


def remove_data(guild):
    for file in os.listdir(SV_PATH):
        if file.startswith(guild.name):
            os.remove(file)

# Local functions:


async def build_link_list(ctx, embed_var, fname, message):
    with open(f'{RES_PATH}/{fname}.json', encoding='utf-8') as rd:
        link_dict = json.loads(rd.read())
    for name, value in {**link_dict[message], **link_dict["all"]}.items():
        embed_var.add_field(name=f'**{name}**', value=value, inline=False)
    await ctx.send(embed=embed_var)


async def set_sv_config(ctx, value, key):
    if os.path.exists(f'{SV_PATH}/{ctx.guild.name}_config.json'):
        with open(f'{SV_PATH}/{ctx.guild.name}_config.json', 'r', encoding='utf-8') as r:
            sv_config = json.loads(r.read())
        if type(value) == dict:
            if key in sv_config:
                sv_config[key].update(value)
            else:
                sv_config.update({key: value})
        else:
            sv_config[key] = value
        with open(f'{SV_PATH}/{ctx.guild.name}_config.json', 'w') as wr:
            wr.write(json.dumps(sv_config))
    else:
        temp_json = json.dumps({key: value})
        with open(f'{SV_PATH}/{ctx.guild.name}_config.json', 'w+') as cr:
            cr.write(temp_json)


def get_valid_text_channel_id(ctx, type_of_data):
    with open(f'{SV_PATH}/{ctx.guild.name}_config.json', encoding='utf-8') as rd:
        message_channel = json.loads(rd.read())[type_of_data]
    return get_text_channel_id_from_name(ctx.guild.name, message_channel)


def get_text_channel_id_from_name(server_name, message_channel):
    sv_text_channel_dict = {}
    keys = []
    values = []
    with open(f"{SV_PATH}/{server_name}.json", encoding='utf-8') as rd:
        sv_data = json.loads(rd.read())["text"]
    for elem in sv_data:
        keys.append(elem.split(" => ")[0])
        values.append(elem.split(" => ")[1])
    for x in range(0, len(keys)):
        sv_text_channel_dict[keys[x]] = values[x]
    return int(sv_text_channel_dict[message_channel])


def get_random_number_unless_specified(question):
    if question == '1':
        return '1'
    elif question == '2':
        return '2'
    return f'{random.randint(1, 8)}'


async def send_pic_or_txt_on_choice(ctx, choice):
    if choice == '1':
        await ctx.send(file=discord.File(random.choice(glob.glob(f"{PIC_PATH}/*.jpg"))))
    elif choice == '2':
        await ctx.send(file=discord.File(random.choice(glob.glob(f"{PIC_PATH}/*.png"))))
    else:
        responses = read_lines(f'{RES_PATH}/responses')
        await ctx.send(f'{random.choice(responses)}')


def env_config():
    token = input(colored("Bot Token: ", "cyan"))
    python_prefix_check = input(colored("OS python 3 cmd command (usually is \"python\"): ", "cyan"))
    raspberry_pi_check = input(colored("Is host raspberry pi (Y/N): ", "cyan")).capitalize()
    while raspberry_pi_check not in ["Y", "N"]:
        raspberry_pi_check = input(
            colored("No such option. Choose ", "cyan") + colored("\"Y\"", "red", attrs=["bold"]) + " or " + colored(
                "\"N\"", "red", attrs=["bold"]) + ":").capitalize()
    with open(f'.env', 'w') as wr:
        wr.write(f"TOKEN=\'{token}\'\nRASPBERRY_PI=\'{raspberry_pi_check}\'\n"
                 f"OS_PYTHON_PREFIX=\'{python_prefix_check}\'")


def sort_dict_by_value(dictionary):
    sorted_values = sorted(dictionary.values(), key=None, reverse=True)  # Sort the values
    sorted_dict = {}
    for i in sorted_values:
        for k in dictionary.keys():
            if dictionary[k] == i:
                sorted_dict[k] = dictionary[k]
                break
    return sorted_dict


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):

        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: youtube_dl.YoutubeDL(YTDL_OPTIONS).extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else youtube_dl.YoutubeDL(YTDL_OPTIONS).prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)
