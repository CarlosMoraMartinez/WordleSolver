from random import sample
from wordle import Wordle

N_GAMES = 1000

class WSolver():
    def __init__(self, game):
        self.game = game
        self.words = game.words

    def chooseWord(self):
        word = sample(self.words, 1).pop()
        print(f"Trying {word}")
        return word

    def playgame(self):
        self.game.reset()
        has_won = False
        while(self.game.canTry() and not has_won):
            word = self.chooseWord()
            n, has_won = self.game.tryWord(word)
        return n, has_won    

def main():
    game = Wordle()
    solver = WSolver(game)
    for i in range(N_GAMES):
        attempts, won = solver.playgame()
        print(f"game {i}: {attempts}, {'WIN' if won else 'LOSE'}. word was {game.word}")

 
if __name__ == "__main__":
    main()       
