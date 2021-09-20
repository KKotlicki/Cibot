import asyncio
import chess
import chess.svg
import io
from cairosvg import svg2png
import discord
import datetime
from discord.ext import commands, tasks
import random
from loguru import logger
from config import SV_PATH, CHESS_OPTIONS, PREFIX
import json
import os.path
from helpers import sort_dict_by_value, set_sv_config, get_valid_text_channel_id
import re


class ChessCog(commands.Cog):
    """Chess commands"""

    def __init__(self, bot):
        self.bot = bot
        self.channel = ''
        self.time_white = 60 * 60
        self.time_black = self.time_white
        self.current_turn = "white"
        """chess time modes. Values in minutes."""
        if not os.path.isfile(f"{SV_PATH}/chess_queue.txt"):
            open(f"{SV_PATH}/chess_queue.txt", "a").close()

    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.command(aliases=['challenge', 'Chess', 'kill', 'ch'])
    async def chess(self, ctx, user: discord.User, time_mode="standard"):
        if user == self.bot.user:
            await ctx.send('Nie umiem grać w szachy')
        elif user.bot:
            await ctx.send('Boty nie potrafią grać w szachy')
        elif user == ctx.author:
            await ctx.send('Nie możesz grać sam ze sobą')
        else:
            await ctx.channel.purge(limit=1)
            if not os.path.exists(f'{SV_PATH}/{ctx.message.guild.name}_config.json'):
                await set_sv_config(ctx, ctx.message.channel.name, 'game')
            if not os.path.exists(f"{SV_PATH}/{ctx.message.guild}_chess.json"):
                with open(f"{SV_PATH}/{ctx.message.guild}_chess.json", "w+") as fn:
                    fn.write("{}")
            if not os.path.exists(f"{SV_PATH}/chess_queue.txt"):
                with open(f"{SV_PATH}/chess_queue.txt", "w+") as fn:
                    fn.write("")
            """Start a chess game with someone!"""
            if time_mode not in CHESS_OPTIONS['time_modes']:
                embed = discord.Embed(title=f"Nie ma takiego trybu gry!",
                                      description=f"Poprawne użycie komendy to: {PREFIX}chess <@użytkownik> [tryb]\n"
                                                  f"Dostępne tryby to:\n",
                                      color=discord.Color.red())
                for key, value in CHESS_OPTIONS['time_modes'].items():
                    if value == 1:
                        lang_genitive_numeral = "minuta"
                    elif type(value) == float or value < 5:
                        lang_genitive_numeral = "minuty"
                    else:
                        lang_genitive_numeral = "minut"
                    embed.description += f"\n**{key}**: {value} {lang_genitive_numeral}"
                await ctx.send(embed=embed)
            elif not get_chess_queue():
                add_to_chess_queue(ctx.author, user, time_mode)
                await chess_loop(ctx.author, user, ctx, self, time_mode)  # Load the loop
            else:
                is_in_queue = False
                for elem in get_chess_queue():
                    if elem[0].split("/id/")[0] == str(ctx.author):
                        is_in_queue = True
                        embed = discord.Embed(title=f"Już wyzwałeś gracza!",
                                              description=f"Zakończ swoją grę z **{elem[1].split('/id/')[0][:-5]}**, "
                                                          f"aby móc wywzać do gry znowu.",
                                              color=discord.Color.red())
                        await ctx.send(embed=embed)
                        break
                if not is_in_queue:
                    add_to_chess_queue(ctx.author, user, time_mode)
                    embed = discord.Embed(title=f"Dodano do kolejki!",
                                          description=f"⚔ Gracz {ctx.author.mention} "
                                                      f"wyzwał gracza {user.mention} na grę w szachy.\n\n"
                                                      f"Wpisz *{PREFIX}chq* aby wyświetlić koljekę.",
                                          color=discord.Color.blue())
                    await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=['chtime', 'ctime', 'ct', 'cht', 'chess_time', 'chesstime', 'game_time'])
    async def chesst(self, ctx):
        await ctx.channel.purge(limit=1)
        if self.switch_timer.is_running():
            white_turn = ""
            black_turn = ""
            if self.current_turn == "white":
                white_turn = "⬅ "
            else:
                black_turn = "⬅ "
            embed = discord.Embed(title=f"⏱ Pozostały czas:",
                                  description=f"Białe - {datetime.timedelta(seconds=self.time_white)} {white_turn}\n"
                                              f"Czarne - {datetime.timedelta(seconds=self.time_black)} {black_turn}",
                                  color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=f"Nikt jeszcze się nie ruszył",
                                  color=discord.Color.blue())
            await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(pass_context=True,
                      aliases=['cqc', 'chess_queue_clear', "clear_chess_queue", "clear_game_queue", "gqc"])
    @commands.has_permissions(administrator=True)
    async def chqc(self, ctx):
        await ctx.channel.purge(limit=1)
        with open(f'{SV_PATH}/chess_queue.txt', 'w+') as fn:
            fn.write('')
            await ctx.send('Kolejka usunięta')
        logger.success(f"@{ctx.author.name} in {ctx.guild.name} removed chess queue.")

    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command()
    async def elo(self, ctx, *, user: discord.User = None):
        try:
            with open(f'{SV_PATH}/{ctx.message.guild.name}_chess.json', encoding='utf-8') as rd:
                json.loads(rd.read())
        except FileNotFoundError:
            await ctx.send('Nie rozegrano jeszcze żadnych partii szachowych.')
            return
        if user is None:
            user = ctx.author
        elo_rating = get_elo(ctx, user, self.bot)
        if elo_rating == 9000:
            elo_rating = "**IT'S OVER 9000!**"
        embed = discord.Embed(title=f'Elo to:',
                              description=f"{user.mention}: {elo_rating}",
                              color=discord.Color.dark_blue())
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['chq', 'chess_queue', 'queuechess', 'game_queue'])
    async def chessq(self, ctx):
        await ctx.channel.purge(limit=1)
        queue = get_chess_queue()
        if not queue:
            embed = discord.Embed(title=f"Kolej gier:",
                                  description=f"🌙 Kolejka jest pusta...\n",
                                  color=discord.Color.dark_blue())
        else:
            embed = discord.Embed(title=f"Kolej gier:",
                                  description=f"⚔ Teraz gra: ***{queue[0][0].split('/id/')[0][:-5]}***"
                                              f"  vs  "
                                              f"***{queue[0][1].split('/id/')[0][:-5]}*** ⚔"
                                              f" - ({queue[0][2]})\n...",
                                  color=discord.Color.blue())
            temp = 1
            for elem in queue:
                if elem != queue[0]:
                    embed.description += f"\n{temp}: *{elem[0].split('/id/')[0][:-5]}* vs " \
                                         f"*{elem[1].split('/id/')[0][:-5]}* - ({elem[2]})"
                    temp += 1
        await ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(aliases=['leaderboard', 'ranking', '10'])
    async def top(self, ctx):
        await ctx.channel.purge(limit=1)
        ranking = {}
        try:
            with open(f'{SV_PATH}/{ctx.message.guild.name}_chess.json', encoding='utf-8') as rd:
                chess_history = json.loads(rd.read())
        except FileNotFoundError:
            await ctx.send('Nie rozegrano jeszcze żadnych partii szachowych.')
            return
        for key in chess_history:
            ranking[key[:-5]] = get_elo(ctx, key, self.bot)
        ranking = sort_dict_by_value(ranking)
        temp = 1
        ranking_list = ''
        for key, value in ranking.items():
            if temp == 1:
                ranking_list += f'👑  **{key}** - **`{value}`**\n'
            else:
                ranking_list += f'\n{temp}. {key} - `{value}`'
            temp += 1
        embed = discord.Embed(title='Ranking szachowy:', description=ranking_list, color=discord.Color.gold())
        await ctx.send(embed=embed)

    @tasks.loop(seconds=1)
    async def switch_timer(self, ctx):
        if self.current_turn == "black" and self.time_black:
            if self.time_black == 1:
                embed = discord.Embed(title="⌛ Czas się skończył!",
                                      description="Dokończ swój ostatni ruch.",
                                      color=discord.Color.blue())
                await ctx.send(embed=embed)
            self.time_black -= 1
        elif self.current_turn == "white" and self.time_white:
            if self.time_black == 1:
                embed = discord.Embed(title="⌛ Czas się skończył!",
                                      description="Dokończ swój ostatni ruch.",
                                      color=discord.Color.blue())
                await ctx.send(embed=embed)
            self.time_white -= 1


async def chess_loop(challenger, challenged, ctx, self, time_mode):
    self.time_white = CHESS_OPTIONS['time_modes'][time_mode] * 60
    self.time_black = CHESS_OPTIONS['time_modes'][time_mode] * 60
    if bool(random.getrandbits(1)):
        user_white = challenger
        user_black = challenged
    else:
        user_black = challenger
        user_white = challenged

    # Chess loop
    embed = discord.Embed(title=f"Nowa gra!",
                          description=f"{user_white.mention} jest białymi, {user_black.mention} jest czarnymi.",
                          color=discord.Color.green())
    await ctx.send(embed=embed)
    # Initiate the board
    board = chess.Board()
    # Save the board as an svg
    svg_img = chess.svg.board(board=board)
    png = svg2png(bytestring=svg_img.encode("UTF-8"))
    png_file = discord.File(io.BytesIO(png), filename="board.png")
    await ctx.send(file=png_file)

    game_over = False
    is_draw_offered = False
    is_timer_set = False
    while game_over is not True:
        # Loop until game is over or canceled.
        cancel = await board_move(user_white, board, ctx, self, is_draw_offered)
        if not is_timer_set:
            self.switch_timer.start(ctx)
            is_timer_set = True
        # Check if game is over
        game_over = board.is_game_over(claim_draw=False)
        result = board.result(claim_draw=True)
        if cancel == "yes":
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"🤝 Remis między {user_white.mention} i {user_black.mention}.",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            self.switch_timer.stop()
            update_match_history(ctx, user_black, user_white, False, self.bot)
            break
        elif cancel == "no":
            is_draw_offered = False
            self.current_turn = "black"
            self.switch_timer.start(ctx)
        elif cancel == "draw":
            is_draw_offered = True
            self.switch_timer.stop()
            embed = discord.Embed(title=f"Propozycja Remisu.",
                                  description=f"{user_white.mention} proponuje remis. "
                                              f"{user_black.mention} czy zgadzasz się? (tak/nie)",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
        elif cancel == "surrender" or cancel == "timeout":
            # Check if a user canceled
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"🎉 {user_black.mention} wygrał! {user_white.mention} poddał się.",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            self.switch_timer.stop()
            update_match_history(ctx, user_black, user_white, True, self.bot)
            break
        elif game_over:
            # Check if game is over
            print(result)
            if result == "1-0":
                embed = discord.Embed(title=f"Gra Zakończona!",
                                      description=f"🎉 {user_white.mention} wygrał! GG",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
                self.switch_timer.stop()
                update_match_history(ctx, user_white, user_black, True, self.bot)
            else:
                embed = discord.Embed(title=f"Gra Zakończona!",
                                      description=f"Remis między {user_white.mention} i {user_black.mention}.",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
                self.switch_timer.stop()
                update_match_history(ctx, user_white, user_black, False, self.bot)
            break
        elif self.time_white == 0:
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"🎉 {user_black.mention} wygrał! "
                                              f"Graczowi {user_white.mention} skończył się czas",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            self.switch_timer.stop()
            update_match_history(ctx, user_black, user_white, True, self.bot)
            break
        else:
            self.current_turn = "black"

        # Basically a repeat of above!
        cancel = await board_move(user_black, board, ctx, self, is_draw_offered)

        game_over = board.is_game_over(claim_draw=False)
        result = board.result(claim_draw=True)
        if cancel == "yes":
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"🤝 Remis między {user_black.mention} i {user_white.mention}.",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            self.switch_timer.stop()
            update_match_history(ctx, user_black, user_white, False, self.bot)
            break
        elif cancel == "no":
            is_draw_offered = False
            self.current_turn = "white"
            self.switch_timer.start(ctx)
        elif cancel == "draw":
            is_draw_offered = True
            self.switch_timer.stop()
            embed = discord.Embed(title=f"Propozycja Remisu",
                                  description=f"{user_black.mention} proponuje remis. "
                                              f"{user_white.mention} czy zgadzasz się? (tak/nie)",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
        elif cancel == "surrender" or cancel == "timeout":
            # Check if a user canceled
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"🎉 {user_white.mention} wygrał! {user_black.mention} poddał się.",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            self.switch_timer.stop()
            update_match_history(ctx, user_white, user_black, True, self.bot)
            break
        elif game_over:
            print(result)
            # Check if game is over
            if result == "0-1":
                embed = discord.Embed(title=f"Gra Zakończona!",
                                      description=f"🎉 {user_black.mention} wygrał! GG",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
                self.switch_timer.stop()
                update_match_history(ctx, user_white, user_black, True, self.bot)
            else:
                embed = discord.Embed(title=f"Gra Zakończona!",
                                      description=f"Remis między {user_black.mention} i {user_white.mention}.",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)
                self.switch_timer.stop()
                update_match_history(ctx, user_white, user_black, False, self.bot)
            break
        elif self.time_black == 0:
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"🎉 {user_white.mention} wygrał! "
                                              f"Graczowi {user_black.mention} skończył się czas",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            self.switch_timer.stop()
            update_match_history(ctx, user_white, user_black, True, self.bot)
            break
        else:
            self.current_turn = "white"
    remove_from_chess_queue()
    if len(get_chess_queue()) != 0:
        local_converter = commands.UserConverter()
        await chess_loop(await local_converter.convert(ctx, get_chess_queue()[0][0].split('/id/')[1]),
                         await local_converter.convert(ctx, get_chess_queue()[0][1].split('/id/')[1]),
                         ctx, self.bot, get_chess_queue()[0][2])


async def board_move(player, board, ctx, self, is_draw_offered):
    # Move loops
    turn_loop = True
    while turn_loop:
        # Make it a loop so if they make a mistake they can have more attempts
        try:
            # Wait for message
            channel_id = get_valid_text_channel_id(ctx, 'game')
            channel = self.bot.get_channel(channel_id)
            message = await self.bot.wait_for("message", check=lambda m: m.author == player and m.channel == channel)

        except asyncio.TimeoutError:
            # That awkward moment they leave you on read (You left them speechless!)
            # Basically we want to cancel the game tbf
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"☠ {player.mention} nie odpowiadał za długo.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return "timeout"
        if is_draw_offered:
            if message.content.lower() == "tak":
                try:
                    delete_array = [message]
                    await ctx.channel.delete_messages(delete_array)
                except Exception as e:
                    print(e)
                    pass
                return "yes"
            elif message.content.lower() in ["nie", "n", "not", "niet", "never"]:
                embed = discord.Embed(title=f"Propozycja odrzucona!",
                                      description=f"{player.mention} odrzucił propozycję remisu.",
                                      color=discord.Color.red())
                await ctx.send(embed=embed)
                try:
                    delete_array = [message]
                    await ctx.channel.delete_messages(delete_array)
                except Exception as e:
                    print(e)
                    pass
                return "no"
        else:
            if message.content.lower() == "surrender":
                try:
                    delete_array = [message]
                    await ctx.channel.delete_messages(delete_array)
                except Exception as e:
                    print(e)
                    pass
                return "surrender"
            elif message.content.lower() == "draw":
                try:
                    delete_array = [message]
                    await ctx.channel.delete_messages(delete_array)
                except Exception as e:
                    print(e)
                    pass
                return "draw"
            else:
                # If they didnt say cancel then lets see if we can play the game!
                try:
                    # We are tying to see if they added a comma split. You can change this i guess!
                    # Moves will be from positions on the board
                    joined = re.sub('[-.></`|{}_,!*^()?+=;:@#$%&~]', '',
                                    re.sub(r'\s+', '', message.content.lower()))\
                        .replace('move', '').replace('from', '').replace('to', '')
                    try:
                        # Get the move
                        if len(joined) >= 4:
                            if ((joined[1] == '7' and joined[3] == '8') or (
                                    joined[1] == '2' and joined[3] == '1')) and board.piece_type_at(chess.parse_square(
                                    joined[0:2])) == 1 and len(joined) == 5:
                                move = chess.Move.from_uci(joined[0:5])
                            elif ((joined[1] == '7' and joined[3] == '8') or (
                                    joined[1] == '2' and joined[3] == '1')) and board.piece_type_at(chess.parse_square(
                                    joined[0:2])) == 1 and len(joined) == 4:
                                move = chess.Move.from_uci(joined[0:4] + 'q')
                            else:
                                move = chess.Move.from_uci(joined[0:4])
                        else:
                            raise ValueError('Szachy: zła długość ruchu')
                        if move in board.legal_moves:
                            # Check if the move was valid
                            embed = discord.Embed(title=f"Ruch",
                                                  description=f"{player.mention} ruszył się: "
                                                              f"`{joined[0:2]} -> {joined[2:4]}`!\n"
                                                              f"Czas Białych - "
                                                              f"{datetime.timedelta(seconds=self.time_white)}\n"
                                                              f"Czas Czarnych - "
                                                              f"{datetime.timedelta(seconds=self.time_black)}",
                                                  color=discord.Color.green())
                            await ctx.send(embed=embed)
                            # Make the move on the board
                            board.push(move)
                            # Remake the image and send it back out!
                            # This is a repeat from earlier
                            svg_img = chess.svg.board(board=board)
                            png = svg2png(bytestring=svg_img.encode("UTF-8"))
                            png_file = discord.File(io.BytesIO(png), filename="board.png")
                            # Send the image
                            await ctx.send(file=png_file)
                            # Stop their turn
                            turn_loop = False
                        else:
                            # If the move wasn't valid
                            embed = discord.Embed(title=f"Error",
                                                  description=f"Niedozwolony ruch ⛔ "
                                                              f"Spróbuj jeszcze raz.",
                                                  color=discord.Color.red())
                            await ctx.send(embed=embed)
                        # Delete the messages to make it a little nicer
                        # This, again, is a copy from above
                        delete_array = [message]
                        try:
                            await ctx.channel.delete_messages(delete_array)
                        except Exception as e:
                            print(e)
                            pass
                    except ValueError:
                        pass
                finally:
                    pass


def get_elo(ctx, user, bot):
    if str(user) == str(bot.user):
        return 9000
    with open(f'{SV_PATH}/{ctx.message.guild.name}_chess.json', encoding='utf-8') as rd:
        chess_history = json.loads(rd.read())
    if str(user) in chess_history.keys():
        player_chess_history = chess_history[str(user)]
        elo_rating = player_chess_history[0] + CHESS_OPTIONS['elo_change_constant'] * (player_chess_history[2] - 1 / (
                1 + 10 ** ((player_chess_history[1] - player_chess_history[0]) / 400)))
        return round(elo_rating)
    else:
        return CHESS_OPTIONS['starting_elo']


def update_match_history(ctx, winner, looser, is_victory, bot):
    with open(f'{SV_PATH}/{ctx.message.guild.name}_chess.json', encoding='utf-8') as rd:
        match_history = json.loads(rd.read())
    if winner not in match_history.keys():
        match_history[str(winner)] = []
    if looser not in match_history.keys():
        match_history[str(looser)] = []
    elo_winner = get_elo(ctx, winner, bot)
    elo_looser = get_elo(ctx, looser, bot)
    if is_victory:
        win = 1
        loss = 0
    else:
        win = 0.5
        loss = 0.5
    match_history[str(winner)] = [elo_winner, elo_looser, win]
    match_history[str(looser)] = [elo_looser, elo_winner, loss]
    with open(f'{SV_PATH}/{ctx.message.guild.name}_chess.json', "w+", encoding='utf-8') as fn:
        fn.write(json.dumps(match_history))


def get_chess_queue():
    chess_queue_lines = []
    chess_queue = []
    with open(f'{SV_PATH}/chess_queue.txt', encoding='utf-8') as rd:
        for line in rd:
            chess_queue_lines.append(line[:-1])
    for elem in chess_queue_lines:
        temp_list = elem.split('/time/')
        temp0 = temp_list[0].split('/vs/')[0]
        temp1 = temp_list[0].split('/vs/')[1]
        temp2 = temp_list[1]
        temp_list = [temp0, temp1, temp2]
        chess_queue.append(temp_list)
    return chess_queue


def add_to_chess_queue(challenger, challenged, time_mode):
    with open(f'{SV_PATH}/chess_queue.txt', 'a', encoding='utf-8') as fn:
        fn.write(f'{challenger}/id/{challenger.id}/vs/{challenged}/id/{challenged.id}/time/{time_mode}\n')


def remove_from_chess_queue():
    with open(f'{SV_PATH}/chess_queue.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open(f'{SV_PATH}/chess_queue.txt', 'w') as fout:
        fout.writelines(data[1:])


def setup(bot):
    bot.add_cog(ChessCog(bot))
