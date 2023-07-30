import random

COLORS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Mastermind:
    num_pegs: int
    num_colors: int
    possibilities: str
    secret_code: str
    guesses: int

    def __init__(self, num_pegs: int = 4, num_colors: int = 6, allow_duplicate: bool = False) -> None:
        self.num_pegs = num_pegs
        self.num_colors = num_colors
        self.possibilities = COLORS[: self.num_colors]
        self.secret_code = (
            self.generate_secret_code_with_duplicate() if allow_duplicate else self.generate_secret_code()
        )
        self.guesses = 0

    def generate_secret_code(self):
        secret = "".join(random.sample(self.possibilities, k=self.num_pegs))
        print(secret)
        return secret

    def generate_secret_code_with_duplicate(self):
        secret = "".join(random.choices(self.possibilities, k=self.num_pegs))
        print(secret)
        return secret

    def check_code(self, guess):
        correct = 0
        wrong = 0
        for i in range(len(self.secret_code)):
            if guess[i] == self.secret_code[i]:
                correct += 1
            elif guess[i] in self.secret_code:
                wrong += 1

        self.guesses += 1
        return (correct, wrong)
