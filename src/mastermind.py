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

        for i in range(len(guess)):
            if guess[i] == secret_code_list[i]:
                correct += 1
                secret_code_list[i] = ""
            elif guess[i] in secret_code_list:
                wrong += 1
                secret_code_list[secret_code_list.index(guess[i])] = ""

        self.guesses += 1
        return (correct, wrong)


class MastermindDuplicate(Mastermind):
    def __init__(self, num_pegs: int = 4, num_colors: int = 6) -> None:
        super().__init__(num_pegs, num_colors)

    def generate_secret_code(self):
        secret = "".join(random.choices(self.possibilities, k=self.num_pegs))
        print(secret)
        return secret
