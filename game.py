import os
import random

from dotenv import load_dotenv
from twitchio.ext import commands

load_dotenv()

TOKEN = os.getenv("TOKEN")
COLORS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
CHANNELS = ["walfleboxbot", "walfask"]


def generate_secret_code(num_pegs, possibilities):
    secret = "".join(random.sample(possibilities, k=num_pegs))
    print(secret)
    return secret


def generate_secret_code_with_duplicate(num_pegs, possibilities):
    secret = "".join(random.choices(possibilities, k=num_pegs))
    print(secret)
    return secret


def provide_feedback(code, guess):
    correct = 0
    wrong = 0
    for i in range(len(code)):
        if guess[i] == code[i]:
            correct += 1
        elif guess[i] in code:
            wrong += 1

    return (correct, wrong)


bot = commands.Bot(token=TOKEN, prefix="!", initial_channels=CHANNELS)


@bot.event
async def event_ready():
    print(f"Bot is ready! {bot.nick}")


is_game_active = False
num_pegs = 0
num_colors = 0
allow_duplicate = None
possibilities = ""
secret_code = ""
guesses = 0


@bot.command(name="game")
@commands.cooldown(rate=1, per=5, bucket=commands.Bucket.channel)
async def start_game(ctx):
    global is_game_active, num_pegs, num_colors, possibilities, secret_code, guesses, allow_duplicate
    if is_game_active:
        await ctx.send("A game is already in progress!")
        return

    try:
        if len(ctx.message.content.split()) >= 4:
            _, num_pegs, num_colors, allow_duplicate = ctx.message.content.split()
        elif len(ctx.message.content.split()) == 3:
            _, num_pegs, num_colors = ctx.message.content.split()
        else:
            num_pegs, num_colors = 4, 6

        num_pegs = int(num_pegs)
        num_colors = int(num_colors)
        possibilities = COLORS[:num_colors]

        if allow_duplicate:
            secret_code = generate_secret_code_with_duplicate(num_pegs, possibilities)
        else:
            secret_code = generate_secret_code(num_pegs, possibilities)

        is_game_active = True
        guesses = 0
        await ctx.send(
            f"""A new Mastermind game has started! Guess the {num_pegs} pegs (code)
              with the possibilities: {possibilities}. Use "!guess ABCD" to make a guess."""
        )
    except ValueError:
        await ctx.send('Invalid command. Use "!game X Y" to start a new game (X: number of pegs, Y: number of colors).')


@bot.command(name="guess")
@commands.cooldown(rate=1, per=5, bucket=commands.Bucket.channel)
async def make_guess(ctx):
    global is_game_active, num_pegs, possibilities, secret_code, guesses
    if not is_game_active:
        await ctx.send(
            'There is no active game. Use "!game X Y" to start a new game (X: number of pegs, Y: number of colors).'
        )
        return

    try:
        _, guess = ctx.message.content.split()
        guess = guess.upper()

        if len(guess) != num_pegs or not all(color in possibilities for color in guess):
            await ctx.send(f"Invalid guess. Please guess {num_pegs} pegs from the provided possibilities.")
            return

        guesses += 1
        feedback = provide_feedback(secret_code, guess)
        if feedback[0] == num_pegs:
            await ctx.send(f"You win! It took you {guesses} guesses to find the code: {''.join(secret_code)}")
            is_game_active = False
        else:
            await ctx.send(f"Guess {guesses}: {str(feedback[0])} correct, {str(feedback[1])} wrong position.")
    except ValueError:
        await ctx.send(f"Invalid guess. Please guess {num_pegs} pegs from the provided possibilities.")


@bot.command(name="gameover")
@commands.cooldown(rate=1, per=5, bucket=commands.Bucket.channel)
async def reset_game(ctx):
    global is_game_active

    if is_game_active:
        is_game_active = False
        await ctx.send(f"Game over... guesses: {guesses}, code: {''.join(secret_code)}")


if __name__ == "__main__":
    bot.run()
