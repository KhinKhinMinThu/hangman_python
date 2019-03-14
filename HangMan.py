# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:57:31 2019

@author: Khin Khin Min Thu
"""
import random

class HangMan:
    
    def __init__(self, category):
        self.word_list = self.loadFile(category)
        self.start_game()
   
    def start_game(self):     
        self.selected_word = self.pick_word() #word for player to guess
        self.display_letters = self.init_letters() #word player is guessing so far
        self.wrong_letters = [] #list of letter playered wrongly guessed
        self.win = False #True is player can guess the whole word correctly
        
    def pick_word(self):
        word = random.choice(self.word_list)
        print('Selected word: ', word, ', Len: ', len(word))
        
         #remove the selected word from the list
        self.word_list.remove(word)
        print('Removed word: ', word, ', Remaining words: ', len(self.word_list))
        return word
    
    def init_letters(self):
        #initialize the list with '_'
        letters = ['_'] * len(self.selected_word)
        print('Display letters: ', letters)
        return letters
        
    def loadFile(self, category):
        word_dir = 'words/'
        with open(word_dir+category+'.txt', 'r') as file:
            word_list = file.read().splitlines()
            
        #print('Total words loaded ('+category+'): ', len(word_list))
        return word_list
    
    def guess_letter(self, letter):
        indices = [i for i, char in enumerate(self.selected_word) if char == letter]
        
        if(len(indices) == 0):
            self.wrong_letters.append(letter)
        else:
            for i in indices:
                self.display_letters[i] = self.selected_word[i]
        
        #player has guessed the word correctly if there is no "_" in the list
        if not '_' in self.display_letters:
            self.win = True
            
        print('Guessed letter: ', letter)
        print('Wrongly guessed letter: ', self.wrong_letters)
        print('Display letter: ', self.display_letters)
        print('Did player win?: ', self.win)
        print('-------------------------------------------------------------------')
        
        
    def display_word(self):
        display_word = " ".join(self.display_letters)
        print('Display word: ', display_word)
        return display_word
        
    def display_wrong_letters(self):
        display_wrong_letters = ", ".join(self.wrong_letters)
        print('Display wrong letters: ', display_wrong_letters)
        return display_wrong_letters
    
#class Hangman:
#    def __init__(self, word_list_file, allowed_guesses=15):
#        self.words = self.read_word_file(word_list_file)
#        self.allowed_guesses = allowed_guesses
#        self.start_game()
#        self.wins = 0
# 
#    def start_game(self):
#        self.secret_word = self.pick_secret_word()
#        self.display_letters = self.create_display_letters()
#        self.guessed_letters = []
#        self.guesses = 0
# 
#    @staticmethod
#    def read_word_file(word_list_file):
#        word_list = []
#        with open(word_list_file, 'r') as f:
#            for line in f:
#                word_list.append(line.rstrip())
#        return word_list
# 
#    def pick_secret_word(self):
#        index = randint(0, len(self.words) - 1)
#        return self.words[index].upper()
# 
#    def create_display_letters(self):
#        letters = []
#        for _ in self.secret_word:
#            letters.append('-')
#        return letters
# 
#    def guess_letter(self, letter):
#        if letter not in self.guessed_letters:
#            guess_wrong = True
#            self.guessed_letters.append(letter)
#            for i in range(len(self.secret_word)):
#                if letter == self.secret_word[i]:
#                    guess_wrong = False
#                    self.display_letters[i] = letter
#            if guess_wrong:
#                self.guesses += 1
# 
#    def check_win(self):
#        word = ''.join(self.display_letters)
#        if word == self.secret_word and self.guesses  self.allowed_guesses
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        