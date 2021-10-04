import random
import emoji
from discord.ext import commands
from config import RES_PATH, PREFIX, BAN_EMOJIS, REACT_AT_RANDOM, REACT_TO_MESSAGE_CONTENT
from helpers import get_random_number_unless_specified, send_pic_or_txt_on_choice, read_lines


class Fun(commands.Cog):
    co_alias = read_lines(f'{RES_PATH}/co_aliases')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=co_alias)
    async def co(self, ctx, *, question=''):
        choice = get_random_number_unless_specified(question)
        await send_pic_or_txt_on_choice(ctx, choice)

    @commands.Cog.listener()
    async def on_message(self, message):
        if BAN_EMOJIS == 'yes' and emoji.emoji_count(message.content) \
                and not message.author.bot and not message.content.startswith(PREFIX):
            ban_emoji_dict = {
                1: '🛑',
                2: '⛔',
                3: '🚫',
                4: '❌',
                5: '😡',
                6: '🤮',
                7: '☠️'
            }
            await message.add_reaction(ban_emoji_dict[random.randint(1, 7)])
            await message.author.send('**W ramach prawnych Konwencji Genewskiej z dnia 15/05/2021 używanie emoji jest '
                                      'zabronione!**\nHttps://www.icrc.org/en / war-and-law / treaties-customary-law /'
                                      ' geneva-conventions / ban-on-emojis\n\n*Zgodnie z ww. dyrektywą i prawem '
                                      'precedensu de iure wykroczenie zostało zgłoszone jako zbrodnia wojenna i '
                                      'przekazana sygnitariuszom wymienionej rady.*\n***Jeżeli winny powtórzy '
                                      'precedens, oskarżenie zostanie przekazana do rewizji i egzekucji z pominięciem '
                                      'walidacji przez Międzynarodowy '
                                      'Trybunał Karny w Hadze.***')
        elif REACT_AT_RANDOM == 'yes' and random.randint(1, 16) == 1 and not message.author.bot \
                and not message.content.startswith(PREFIX):
            emoji_dict = {
                1: "👍",
                2: "❤",
                3: "🙂",
                4: "🤯",
                5: "👀",
                6: "🧠",
                7: "🫀",
                8: "🧐",
                9: "🥳",
                10: "😀",
                11: "😮",
                12: "🎓",
                13: "⭐",
                14: "☢",
                15: "☣",
                16: "🧡",
                17: "💛",
                18: "💚",
                19: "💙",
                20: "💜",
                21: "🖤",
                22: "🤍",
                23: "😃",
                24: "😄",
                25: "😲"
            }
            await message.add_reaction(emoji_dict[random.randint(1, 16)])
        elif message.content.lower() in REACT_TO_MESSAGE_CONTENT:
            ctx = await self.bot.get_context(message)
            await ctx.send("A co to K*rwa jest?!")


def setup(bot):
    bot.add_cog(Fun(bot))
