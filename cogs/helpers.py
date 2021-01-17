import random
import discord
from config import *
import glob


def read_file(file_name):
    with open(f"{file_name}.txt") as rs:
        return rs.read().splitlines()


# Local functions:

def get_random_number_unless_specified(question):
    if question == '1':
        return '1'
    elif question == '2':
        return '2'
    return f'{random.randint(1, 8)}'


async def send_pic_or_txt_on_choice(ctx, choice):
    if choice == '1':
        await ctx.send(file=discord.File(random.choice(glob.glob(f"{pic_dir}/*.jpg"))))
    elif choice == '2':
        await ctx.send(file=discord.File(random.choice(glob.glob(f"{pic_dir}/*.png"))))
    else:
        responses = read_file(f'{res_dir}/responses')
        await ctx.send(f'{random.choice(responses)}')
