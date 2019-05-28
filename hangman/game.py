from .exceptions import *
from random import choice

class GuessAttempt(object):
    def __init__(self,attempt,hit=False,miss=False):
        self.attempt = attempt
        self.hit = hit
        self.miss = miss
        
        if hit and miss:
            raise InvalidGuessAttempt()
            
    def is_hit(self):
        if self.hit:
            return True
        if self.miss:
            return False
        
    def is_miss(self):
        if self.miss:
            return True
        if self.hit:
            return False


class GuessWord(object):
    def __init__(self,word):
        self.answer = word.lower()
        self.masked = '*' * len(word)
        
        if self.answer == '':
            raise InvalidWordException()
            
    def perform_attempt(self,letter):
        self.letter = letter.lower()
        
        if len(self.letter) > 1:
            raise InvalidGuessedLetterException()
            
        if self.letter in self.answer:
            attempt = GuessAttempt(letter, hit=True)

        if self.letter not in self.answer:
            attempt = GuessAttempt(letter, miss=True)
        
        index = 0
        new_masked = ''
        for char in self.answer:

            if char == self.letter:
                new_masked += self.letter
            else:
                new_masked += self.masked[index]
            index += 1

        self.masked = new_masked
        
        return attempt

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self,list_of_words=WORD_LIST,number_of_guesses=5):
        self.list_of_words = list_of_words
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.word = GuessWord(self.select_random_word(list_of_words))
    
    @classmethod
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException
        return choice(list_of_words)
    
    def guess(self, letter):

        if self.is_won() or self.is_lost():
            raise GameFinishedException()

        letter = letter.lower()
        self.word.perform_attempt(letter)
        self.previous_guesses.append(letter)

        if self.word.perform_attempt(letter).is_miss():
            self.remaining_misses -= 1

        if self.word.answer == self.word.masked:
            raise GameWonException()

        if self.remaining_misses == 0:
            raise GameLostException()

        return self.word.perform_attempt(letter)
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False

    def is_lost(self):
        if self.remaining_misses == 0:
            return True
        return False

    def is_finished(self):
        if self.word.answer == self.word.masked or self.remaining_misses == 0:
            return True
        return False

