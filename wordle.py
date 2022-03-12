from random import sample
import unidecode

DICT_FILE = "diccionario.txt"
CHEATING = True

OTHER_ORDER = "*"
CORRECT = "^"
WRONG = "_"

class Wordle:    
    """
	The Wordle game. With this script you can play from the console.
    """
    def __init__(self, dict_file = DICT_FILE, wordsize = 5, max_attempts = 6):
        self.wordsize = wordsize
        self.max_attempts = max_attempts
        self.words = self.read_dict(dict_file, wordsize)
        self.attempts = 0
        self.failed_letters = set()
        self.misplaced_letters = dict()
        self.tried_words = []
        self.state = "_"*self.wordsize
        self.word = ""
    @staticmethod
    def read_dict(dict_file, wordsize):
        words = [i.strip().upper() for i in open(dict_file, 'r') if len(i.strip()) == wordsize]
        words = [unidecode.unidecode(i) for i in words]
        return words
        
    def reset(self):
        self.attempts = 0
        self.failed_letters = set()
        self.misplaced_letters = dict()
        self.state = "_"*self.wordsize
        self.word = sample(self.words, 1).pop()
        self.tried_words = []
    def canTry(self):
        return self.attempts < self.max_attempts
    def hasWon(self):
        return self.state == self.word
    def tryWord(self, word):
        if self.attempts >= self.max_attempts:
            return -1, False
        self.attempts += 1
        if len(word) != self.wordsize:
            return -1, False
        if word == self.word:
            self.state = self.word         
            return self.attempts, True
        else:
            wordstate = "_"*self.wordsize
            for i, a, b in zip(range(self.wordsize), word, self.word):
                if a == b:
                    self.state = self.state[:i] + a + self.state[i + 1:]
                    wordstate = wordstate[:i] + a + wordstate[i + 1:]
                elif a in self.word:
                    aux = self.misplaced_letters.setdefault(a, set())
                    aux.add(i)
                    wordstate = wordstate[:i] + OTHER_ORDER + wordstate[i + 1:]
                else:
                    self.failed_letters.add(a)
            self.tried_words.append((word, wordstate))
            return self.attempts, False
    def printInfo(self):
        print(f"Letras descartadas: {', '.join(self.failed_letters)}")
        print(f"Letras mal colocadas: {', '.join(self.misplaced_letters)}")
        print(f"Posiciones probadas para cada letra: ")
        print(self.misplaced_letters)
        palabrasprobadas = ''.join([i + '\n' + j + '\n--\n' for i, j in self.tried_words])
        print(f"Palabras probadas:\n{palabrasprobadas}")
        print(f"{self.state}  - ({self.attempts} de {self.max_attempts} intentos)")
        if CHEATING:
                print("palabra (cheating ON): " + self.word)        
    def play_console(self):
        self.reset()
        has_won = False
        while(self.canTry() and not has_won):
            self.printInfo()
            word = input(f"Prueba una palabra de {self.wordsize} letras:)\n").upper()
            word = unidecode.unidecode(word)
            n, has_won = self.tryWord(word)
        self.endGame(has_won)
        return n, has_won
    def endGame(self, has_won):
        if has_won:
            print(f"YOU WON IN {self.attempts} ATTEMPTS\n\n")
        else:
           print(f"YOU LOSE. THE WORD WAS {self.word}\n\n")

        
def main():
    game = Wordle(DICT_FILE)
    while(True):
        game.play_console()
        print("*** NEW GAME ***")

 
if __name__ == "__main__":
    main()       
               

