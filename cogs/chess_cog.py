import asyncio
import chess
import chess.svg
import discord
from discord.ext import commands
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg
from PIL import Image
import random


class ChessCog(commands.Cog):
    """Chess commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def chess(self, ctx, *, user: discord.User):
        """Start a chess game with someone!"""
        await chess_loop(ctx.author, user, ctx, self.bot)  # Load the loop


async def chess_loop(challenger, challenged, ctx, bot):

    if bool(random.getrandbits(1)):
        user1 = challenger
        user2 = challenged
    else:
        user2 = challenger
        user1 = challenged

    # Chess loop
    embed = discord.Embed(title=f"Nowa gra!",
                          description=f"Wiadomości w DM. {user1.mention} jest białymi, {user2.mention} jest czarnymi.",
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
        # Loop until game is over or canceled. Yes this can be optimized but this was around the time he didnt pay
        cancel = await board_move(user1, board, ctx, bot)
        # Check if game is over
        game_over = board.is_game_over(claim_draw=False)
        if cancel:
            # Check if a user canceled
            return
        if game_over:
            # Check if game is over
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"{user1.mention} wygrał! GG",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            return

        # Basically a repeat of above!
        cancel = await board_move(user2, board, ctx, bot)
        game_over = board.is_game_over(claim_draw=False)
        if cancel:
            return
        if game_over:
            embed = discord.Embed(title=f"Gra Zakończona!",
                                  description=f"{user2.mention} wygrał! GG",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
            return


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
                    move = chess.Move.from_uci(joined)
                    if move in board.legal_moves:
                        # Check if the move was valid
                        print(joined[0:2])
                        print(joined[2:4])
                        embed = discord.Embed(title=f"Ruch",
                                              description=f"{player.mention} ruszył się z {joined[0:2]} do {joined[2:4]}!",
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
                                              description=f"Nielegalny ruch :no_entry:"
                                                          f"Spróbuj jeszcze raz.",
                                              color=discord.Color.red())
                        await player.send(embed=embed)
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


def setup(bot):
    bot.add_cog(ChessCog(bot))
