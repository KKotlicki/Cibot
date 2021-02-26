import asyncio
import chess
import chess.svg
import discord
from discord.ext import commands
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from PIL import Image
import random
from config import sv_dir, chess_options
import json
import os.path
from helpers import sort_dict_by_value


class ChessCog(commands.Cog):
    """Chess commands"""

    def __init__(self, bot):
        self.bot = bot
        if not os.path.isfile(f"{sv_dir}/chess_queue.txt"):
            open(f"{sv_dir}/chess_queue.txt", "a").close()

    @commands.command()
    async def chess(self, ctx, *, user: discord.User):
        if not os.path.isfile(f"{sv_dir}/{ctx.message.guild}_chess.json"):
            with open(f"{sv_dir}/{ctx.message.guild}_chess.json", "w+") as fn:
                fn.write("{}")
        """Start a chess game with someone!"""
        if not get_chess_queue():
            add_to_chess_queue(ctx.author, user)
            await chess_loop(ctx.author, user, ctx, self.bot)  # Load the loop
        else:
            is_in_queue = False
            for elem in get_chess_queue():
                if elem[0].split("/id/")[0] == str(ctx.author):
                    is_in_queue = True
                    embed = discord.Embed(title=f"Już wyzwałeś gracza!",
                                          description=f"Zakończ swoją grę z **{elem[1][:-5]}** aby móc wywzać do gry znowu.",
                                          color=discord.Color.green())
                    await ctx.send(embed=embed)
                    break
            if not is_in_queue:
                add_to_chess_queue(ctx.author, user)
                embed = discord.Embed(title=f"Dodano do kolejki!",
                                      description=f"Gracz {ctx.author} wyzwał gracza {user.mention} na grę w szachy.",
                                      color=discord.Color.green())
                await ctx.send(embed=embed)

    @commands.command()
    async def elo(self, ctx, *, user: discord.User = None):
        # try:
        if user is None:
            user = ctx.author
        elo_rating = get_elo(ctx, user)
        embed = discord.Embed(title=user.mention,
                              description=f"Elo to: {elo_rating}",
                              color=discord.Color.green())
        await ctx.send(embed=embed)
        # except:
        # print("elo error")

    @commands.command()
    async def top(self, ctx):
        ranking = {}
        with open(f'{sv_dir}/{ctx.message.guild.name}_chess.json', encoding='utf-8') as rd:
            chess_history = json.loads(rd.read())
        for key in chess_history:
            ranking[key[:-5]] = get_elo(ctx, key)
        ranking = sort_dict_by_value(ranking)
        embed = discord.Embed(title='Leaderboard:', color=discord.Color.green())
        temp = 1
        for key, value in ranking.items():
            if temp == 1:
                embed.add_field(name=f'1.  :crown:  **{key}**  :crown:', value=f'**`{value}`**', inline=False)
            else:
                embed.add_field(name=f'{temp}. {key}', value=f'`{value}`', inline=False)
            temp += 1
        await ctx.send(embed=embed)


async def chess_loop(challenger, challenged, ctx, bot):
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
    img = chess.svg.board(board=board)
    outputfile = open('chess_board.svg', "w")
    outputfile.write(img)
    outputfile.close()
    # Convert svg to png
    drawing = svg2rlg("chess_board.svg")
    renderPM.drawToFile(drawing, "chess_board.png", fmt="PNG")
    img = Image.open('chess_board.png')
    img.save('chess_board.png')
    # Send the chess board
    await ctx.send(file=discord.File(fp="chess_board.png"))
    game_over = False
    while game_over is not True:
        # Loop until game is over or canceled.
        cancel = await board_move(user_white, board, ctx, bot)
        # Check if game is over
        game_over = board.is_game_over(claim_draw=False)
        if cancel:
            # Check if a user canceled
            break
        if game_over:
            # Check if game is over
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"{user_white.mention} wygrał! GG",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            update_match_history(ctx, user_white, user_black, True)
            break

        # Basically a repeat of above!
        cancel = await board_move(user_black, board, ctx, bot)
        game_over = board.is_game_over(claim_draw=False)
        if cancel:
            break
        if game_over:
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"{user_black.mention} wygrał! GG",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            update_match_history(ctx, user_black, user_white, True)
            break
    remove_from_chess_queue()
    if len(get_chess_queue()) != 0:
        local_converter = commands.UserConverter()
        await chess_loop(await local_converter.convert(ctx, get_chess_queue()[0][0].split('/id/')[1]),
                         await local_converter.convert(ctx, get_chess_queue()[0][1].split('/id/')[1]), ctx, bot)


async def board_move(player, board, ctx, bot):
    # Move loops
    turn_loop = True
    while turn_loop:
        # Make it a loop so if they make a mistake they can have more attempts
        try:
            # Wait for message
            message = await bot.wait_for("message", check=lambda m: m.author == player)
        except asyncio.TimeoutError:
            # That awkward moment they leave you on read (You left them speechless!)
            # Basically we want to cancel the game tbf
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"{player.mention} nie odpowiadał za długo.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        if message.content.lower() == "cancel":
            # If the message was cancel, then cancel...
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"{player.mention} zakończył grę.",
                                  color=discord.Color.red())
            await ctx.send(embed=embed)
            # Delete their messages to make it a little nicer
            delete_array = [message]
            try:
                await ctx.channel.delete_messages(delete_array)
            except Exception as e:
                print(e)
                pass
            return True
        else:
            # If they didnt say cancel then lets see if we can play the game!
            try:
                # We are tying to see if they added a comma split. You can change this i guess!
                # Moves will be from positions on the board
                joined = message.content
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
                                              description=f"{player.mention} ruszył się: {joined[0:2]} :arrow_right: {joined[2:4]}!",
                                              color=discord.Color.green())
                        await ctx.send(embed=embed)
                        # Make the move on the board
                        board.push(move)
                        # Remake the image and send it back out!
                        # This is a repeat from earlier
                        img = chess.svg.board(board=board)
                        outputfile = open('chess_board.svg', "w")
                        outputfile.write(img)
                        outputfile.close()
                        drawing = svg2rlg("chess_board.svg")
                        renderPM.drawToFile(drawing, "chess_board.png", fmt="PNG")
                        # Send the image
                        await ctx.send(file=discord.File(fp="chess_board.png"))
                        # Stop their turn
                        turn_loop = False
                    else:
                        # If the move wasn't valid
                        embed = discord.Embed(title=f"Error",
                                              description=f"Nielegalny ruch :no_entry: "
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


def get_elo(ctx, user):
    with open(f'{sv_dir}/{ctx.message.guild.name}_chess.json', encoding='utf-8') as rd:
        chess_history = json.loads(rd.read())
    if str(user) in chess_history.keys():
        player_chess_history = chess_history[str(user)]
        elo_rating = player_chess_history[0] + chess_options['K'] * (player_chess_history[2] - 1 / (
                1 + 10 ** ((player_chess_history[1] - player_chess_history[0]) / 400)))
        return round(elo_rating)
    else:
        return chess_options['starting_elo']


def update_match_history(ctx, winner, looser, is_victory):
    with open(f'{sv_dir}/{ctx.message.guild.name}_chess.json', encoding='utf-8') as rd:
        match_history = json.loads(rd.read())
    if winner not in match_history.keys():
        match_history[str(winner)] = []
    if looser not in match_history.keys():
        match_history[str(looser)] = []
    elo_winner = get_elo(ctx, winner)
    elo_looser = get_elo(ctx, looser)
    if is_victory:
        win = 1
        lost = 0
    else:
        win = 0.5
        lost = 0.5
    match_history[str(winner)] = [elo_winner, elo_looser, win]
    match_history[str(looser)] = [elo_looser, elo_winner, lost]
    with open(f'{sv_dir}/{ctx.message.guild.name}_chess.json', "w+", encoding='utf-8') as fn:
        fn.write(json.dumps(match_history))


def get_chess_queue():
    chess_queue_lines = []
    chess_queue = []
    with open(f'{sv_dir}/chess_queue.txt', encoding='utf-8') as rd:
        for line in rd:
            chess_queue_lines.append(line[:-1])
    for elem in chess_queue_lines:
        chess_queue.append(elem.split('/vs/'))
    return chess_queue


def add_to_chess_queue(challenger, challenged):
    with open(f'{sv_dir}/chess_queue.txt', 'a', encoding='utf-8') as fn:
        fn.write(f'{challenger}/id/{challenger.id}/vs/{challenged}/id/{challenged.id}\n')


def remove_from_chess_queue():
    with open(f'{sv_dir}/chess_queue.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    with open(f'{sv_dir}/chess_queue.txt', 'w') as fout:
        fout.writelines(data[1:])


def setup(bot):
    bot.add_cog(ChessCog(bot))
