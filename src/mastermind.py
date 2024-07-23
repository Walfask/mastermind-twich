import random

COLORS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Mastermind:
    num_pegs: int
    num_colors: int
    possibilities: str
    secret_code: str
    guesses: int

    def __init__(self, num_pegs: int = 4, num_colors: int = 6) -> None:
        self.num_pegs = num_pegs
        self.num_colors = num_colors
        self.possibilities = COLORS[: self.num_colors]
        self.secret_code = self.generate_secret_code()
        self.guesses = 0

    def generate_secret_code(self):
        secret = "".join(random.sample(self.possibilities, k=self.num_pegs))
        print(secret)
        return secret

    def check_code(self, guess):
        correct = 0
        wrong = 0
        secret_code_list = list(self.secret_code)

        wrong = len(set.intersection(set(guess), set(self.secret_code)))

        for i, v in enumerate(guess):
            if v == secret_code_list[i]:
                correct += 1
                wrong -= 1
                secret_code_list[i] = ""

        self.guesses += 1
        return (correct, wrong)


class MastermindDuplicate(Mastermind):
    def __init__(self, num_pegs: int = 4, num_colors: int = 6) -> None:
        super().__init__(num_pegs, num_colors)

    def generate_secret_code(self):
        secret = "".join(random.choices(self.possibilities, k=self.num_pegs))
        print(secret)
        return secret

    def check_code(self, guess_raw):
        secret_code = list(self.secret_code)
        guess = list(guess_raw)
        correct = 0
        wrong = 0

        for i, v in enumerate(secret_code):
            if guess[i] == v:
                guess[i] = "6"
                secret_code[i] = "7"
                correct += 1

        for i, v in enumerate(guess):
            try:
                index = secret_code.index(v)
                secret_code[index] = "3"
                wrong += 1
            except ValueError:
                continue

        self.guesses += 1
        return (correct, wrong)
