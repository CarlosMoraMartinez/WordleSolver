import sys
from random import sample

from wordle import *

N_GAMES = 1000
METHOD = 8 #This sets the algorithm to choose the next word

"""
Scores for each method out of 1000 trials:

1	0.002	4.0
2	0.071	5.14
3	0.525	4.91
4	0.117	5.0
5	0.23	4.96
6	0.912	4.33
7	0.855	4.59
8	0.921	4.07
9	0.929	4.22
10	0.944	4.01

Using reversed ordering:

6	0.918	4.32
8	0.657	5.03
9	0.659	4.76
10	0.665	4.76

Using 1/ of sorted dictionary:

6	0.918	4.27
8	0.936	4.06
9	0.883	4.32
10	0.911	4.41


"""

class WSolver():
    def __init__(self, game, configure = 1):
        self.game = game
        self.words = game.words
        self.n = 0
        self.word = ""
        self.has_won = False
        configs = {1: self.chooseWord_random, 
                   2: self.chooseWord_score, 
                   3:self.chooseWord_scoreAndState, 
                   4:self.chooseWord_state,
                   5:self.chooseWord_possible,
                   6:self.chooseWord_ScoreStateAndPossible,
                   7:self.chooseWord_orderOnly,
                   8:self.chooseWord_orderSet,
                   9:self.chooseWord_basedOnMove1,
                   10:self.chooseWord_basedOnMove2
                   }
        setattr(self, "chooseWord", configs[configure])
        self.data = dict()
    
    @staticmethod
    def removeWordsWithDiscardedLetters(words, letters):
        """ This alone succeedes around 7% times """
        #print(letters)
        if(not letters):
            return words
        hasit = lambda w : not any([True if l in w else False for l in letters])
        newwords = list(filter(hasit, words))
        return newwords      

    @staticmethod
    def checkWithState(words, state):
        """ This alone succeedes around 10% times """
        print(state)
        if(state.count(WRONG) == len(state)):
            return words
        compatible = lambda word : all([True if w == s or s == WRONG else False for w, s in zip(word, state)])
        newwords = list(filter(compatible, words))
        return newwords

    @staticmethod
    def checkPresentLetters(words, letters_present):
         """ This alone succeedes around 20% times """
         newwords = []
         for w in words:
             possible = True
             for letra, poss in letters_present.items():
                 if letra in w:
                     for p in poss:
                         if w[p] == letra:
                             possible = False #Si la letra esta en una de las posiciones descartadas
                             break
                 else:
                     possible = False #Si la letra no esta 
                     break
             if possible:
                 newwords.append(w)
         return newwords

    @staticmethod
    def orderwords_basedOnCount(words):
        alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
        allwords = ''.join(words)
        alphacount = {l:allwords.count(l) for l in alphabet}
        #print("LETTERS: ", alphacount)
        scores = [sum([alphacount[i] for i in w]) for w in words]
        sortedwords = sorted(zip(scores, words), reverse = True)
        if(len(sortedwords) < 10):
            print("WORD SCORES: ", sortedwords)
        return [j for i, j in sortedwords]

    @staticmethod
    def orderwords_basedOnCountSet(words):
        alphabet = "abcdefghijklmnopqrstuvwxyz".upper()
        allwords = ''.join(words)
        alphacount = {l:allwords.count(l) for l in alphabet}
        #print("LETTERS: ", alphacount)
        scores = [sum([alphacount[i] for i in set(w)]) for w in words]
        sortedwords = sorted(zip(scores, words), reverse = True)
        if(len(sortedwords) < 10):
            print("WORD SCORES: ", sortedwords)
        return [j for i, j in sortedwords]
    
    @staticmethod
    def countUniqueVocals(word):
        return len(set([i for i in word if i in 'AEIOU']))

    @staticmethod
    def countVocals(word):
        return len([i for i in word if i in 'AEIOU'])

    @staticmethod
    def getVocals(word):
        return [i for i in word if i in 'AEIOU']

    def chooseWord_random(self):
        """ This alone succeedes around 0.1% times """
        word = sample(self.words, 1).pop()
        return word
    
    def chooseWord_score(self):
        """ This alone succeedes around 7% times """
        self.words = self.removeWordsWithDiscardedLetters(self.words, self.game.failed_letters)
        return self.chooseWord_random()

    def chooseWord_scoreAndState(self):
        """ This alone succeedes around 50% times """
        self.words = self.removeWordsWithDiscardedLetters(self.words, self.game.failed_letters)
        self.words = self.checkWithState(self.words, self.game.state)
        return self.chooseWord_random()

    def chooseWord_state(self):
        """ This alone succeedes around 10% times """
        self.words = self.checkWithState(self.words, self.game.state)
        return self.chooseWord_random()

    def chooseWord_possible(self):
        """ This alone succeedes around 20% times """
        self.words = self.checkPresentLetters(self.words, self.game.misplaced_letters)
        return self.chooseWord_random()

    def chooseWord_ScoreStateAndPossible(self):
        """ This alone succeedes around 90% times """
        self.words = self.checkWithState(self.words, self.game.state)
        self.words = self.checkPresentLetters(self.words, self.game.misplaced_letters)
        self.words = self.removeWordsWithDiscardedLetters(self.words, self.game.failed_letters)
        return self.chooseWord_random()

    def chooseWord_orderOnly(self):
        """ This alone succeedes around 85.5% times. Worse than without sorting"""
        self.words = self.checkWithState(self.words, self.game.state)
        self.words = self.checkPresentLetters(self.words, self.game.misplaced_letters)
        self.words = self.removeWordsWithDiscardedLetters(self.words, self.game.failed_letters)
        self.words = self.orderwords_basedOnCount(self.words)
        return self.words[0]

    def chooseWord_orderSet(self):
        """ This alone succeedes around 92-94% """
        self.words = self.checkWithState(self.words, self.game.state)
        self.words = self.checkPresentLetters(self.words, self.game.misplaced_letters)
        self.words = self.removeWordsWithDiscardedLetters(self.words, self.game.failed_letters)
        self.words = self.orderwords_basedOnCountSet(self.words)
        return self.words[0]

    def chooseWord_basedOnMove1(self):
        """ This alone succeedes around 85% """
        #print(f"CHOOSING: {self.n} : {self.data}")
        if(self.n == 0):
            wlist = []
            for w in self.words:
                vocals = self.getVocals(w)
                if len(vocals) == len(set(vocals)) and len(set(vocals)) == 3: 
                    #print(f"adding {w}, with vocals {''.join(vocals)}")
                    wlist.append(w)
            words = self.orderwords_basedOnCountSet(wlist)
            self.data.setdefault("vocals", set(self.getVocals(words[0])))  
            return words[0]
        elif(self.n == 1):
            self.words = self.removeWordsWithDiscardedLetters(self.words, self.game.failed_letters)
            wlist = []
            #Get words which complete vocals
            for w in self.words:
                word_vocals = self.getVocals(w)
                vocals = self.data['vocals'].union(set(word_vocals))
                if len(vocals) == 5 and len(set(word_vocals)) == len(word_vocals):
                    #print(f"adding {w}, with vocals {''.join(vocals)}")
                    wlist.append(w)
            if wlist:
                words = self.orderwords_basedOnCountSet(wlist)
                return words[0]
            else:
                print("STEP 1: NOT WORDS WITH ENOUGH VOCALS") #should not happen
                self.words = self.checkWithState(self.words, self.game.state)
                self.words = self.checkPresentLetters(self.words, self.game.misplaced_letters)
                self.words = self.orderwords_basedOnCountSet([w for w in self.words if 'O' in w and 'U' in w])    
                return self.words[0]                                
        else:
            self.words = self.checkWithState(self.words, self.game.state)
            self.words = self.checkPresentLetters(self.words, self.game.misplaced_letters)
            self.words = self.removeWordsWithDiscardedLetters(self.words, self.game.failed_letters)  
            self.words = self.orderwords_basedOnCountSet(self.words)     
            if(self.words):
                return self.words[0]
            else:
                print("STEP >= 2: NOT WORDS WITH ENOUGH VOCALS") #should not happen
                return "Z"*self.game.wordsize

    def chooseWord_basedOnMove2(self):
        """ This alone succeedes around 92% """
        #print(f"CHOOSING: {self.n} : {self.data}")
        if(self.n == 0):
            wlist = []
            for w in self.words:
                vocals = self.getVocals(w)
                if len(vocals) == len(set(vocals)) and len(set(vocals)) == 3: 
                    #print(f"adding {w}, with vocals {''.join(vocals)}")
                    wlist.append(w)
            words = self.orderwords_basedOnCountSet(wlist)
            self.data.setdefault("vocals", set(self.getVocals(words[0])))  
            return words[0]                           
        else:
            self.words = self.checkWithState(self.words, self.game.state)
            self.words = self.checkPresentLetters(self.words, self.game.misplaced_letters)
            self.words = self.removeWordsWithDiscardedLetters(self.words, self.game.failed_letters)    
            self.words = self.orderwords_basedOnCountSet(self.words)   
            return self.words[0]
   
    def playgame(self):
        self.game.reset()
        self.words = self.game.words
        self.has_won = False
        self.n = 0
        while(self.game.canTry() and not self.has_won):
            self.word = self.chooseWord()
            print(f"{self.game.attempts}: Trying {self.word} (answer = {self.game.word}) in state {self.game.state}, with discarded {self.game.failed_letters} and misplaced {self.game.misplaced_letters}. Space of {len(self.words)} words")
            if(len(self.words) < 10):
                print("NOT DISCARDED YET: ", ", ".join(self.words))
            self.n, self.has_won = self.game.tryWord(self.word)
        return self.n, self.has_won    


def run(method):
    game = Wordle()
    solver = WSolver(game, method)
    won_games = media = 0
    attempt_list = []
    
    for i in range(N_GAMES):
        attempts, won = solver.playgame()
        if won:
            won_games += 1
            attempt_list.append(attempts)
            media = round(sum(attempt_list)/len(attempt_list),2)
        print(f"game {i}: {attempts}, {'WIN' if won else 'LOSE'}. word was {game.word}. Won {won_games}/{i + 1}. Mean attempts = {media}\n*****\n")
    return won_games/(i + 1), media

def main():
    method = sys.argv[1].split(",") if len(sys.argv) > 1 else [ METHOD ]
    results = []
    for m in method:
        won, media = run(int(m))
        results.append([m, won, media])
    print('\n'.join(['\t'.join([str(l) for l in i]) for i in results]))
    

 
if __name__ == "__main__":
    main()       
