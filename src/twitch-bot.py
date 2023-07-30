import json
import os
import random

from dotenv import load_dotenv
from twitchio.ext import commands

from mastermind import Mastermind

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNELS = json.loads(os.getenv("CHANNELS"))
NOT_GAME_MESSAGES = json.loads(os.getenv("MESSAGES"))


bot = commands.Bot(token=TOKEN, prefix="!", initial_channels=CHANNELS)
channel_game_settings = {}


@bot.event
async def event_ready():
    print(f"Bot is ready! {bot.nick}")


@bot.command(name="game")
@commands.cooldown(rate=1, per=5, bucket=commands.Bucket.channel)
async def start_game(ctx):
    global channel_game_settings
    if ctx.channel.name in channel_game_settings:
        await ctx.send("A game is already in progress!")
        return

    try:
        if len(ctx.message.content.split()) >= 4:
            _, num_pegs, num_colors = ctx.message.content.split()
            allow_duplicate = True
        elif len(ctx.message.content.split()) == 3:
            _, num_pegs, num_colors = ctx.message.content.split()
            allow_duplicate = False
        else:
            num_pegs, num_colors, allow_duplicate = 4, 6, False

        num_pegs = int(num_pegs)
        num_colors = int(num_colors)
        channel_game_settings[ctx.channel.name] = Mastermind(num_pegs, num_colors, allow_duplicate)

        await ctx.send(
            f"""A new Mastermind game has started! Guess the {num_pegs} pegs (code)
              with the possibilities: {channel_game_settings[ctx.channel.name].possibilities}.
              Use "!guess ABCD" to make a guess."""
        )
    except ValueError:
        await ctx.send('Invalid command. Use "!game X Y" to start a new game (X: number of pegs, Y: number of colors).')


@bot.command(name="guess")
@commands.cooldown(rate=1, per=5, bucket=commands.Bucket.channel)
async def make_guess(ctx):
    global channel_game_settings
    game = channel_game_settings.get(ctx.channel.name)

    if not game:
        await ctx.send(
            'There is no active game. Use "!game X Y" to start a new game (X: number of pegs, Y: number of colors).'
        )
        return

    try:
        _, guess = ctx.message.content.split()
        guess = guess.upper()

        if len(guess) != game.num_pegs or not all(color in game.possibilities for color in guess):
            await ctx.send(
                f"""Invalid guess. Please guess {game.num_pegs} pegs from
                the provided possibilities: {game.possibilities}"""
            )
            return

        feedback = game.check_code(guess)

        if feedback[0] == game.num_pegs:
            await ctx.send(f"You win! It took you {game.guesses} guesses to find the code: {''.join(game.secret_code)}")
            del channel_game_settings[ctx.channel.name]
        else:
            await ctx.send(f"Guess {game.guesses}: {str(feedback[0])} correct, {str(feedback[1])} wrong position.")
    except ValueError:
        await ctx.send(f"Invalid guess. Please guess {game.num_pegs} pegs from the provided possibilities.")


@bot.command(name="gameover")
@commands.cooldown(rate=1, per=5, bucket=commands.Bucket.channel)
async def reset_game(ctx):
    global channel_game_settings
    game = channel_game_settings.get(ctx.channel.name)

    if game:
        await ctx.send(f"Game over... after {game.guesses} guesses, the code was: {''.join(game.secret_code)}")
        del channel_game_settings[ctx.channel.name]


@bot.command(name="notgame")
@commands.cooldown(rate=1, per=5, bucket=commands.Bucket.channel)
async def not_game(ctx):
    message = random.choices(NOT_GAME_MESSAGES, k=1)[0]
    await ctx.send(message)


if __name__ == "__main__":
    bot.run()
