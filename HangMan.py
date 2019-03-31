# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:57:31 2019

@author: Khin Khin Min Thu
"""
import random

class HangMan:
    score = 0    
    def __init__(self, category, wrong_guesses_allowed=6):
        self.word_list = self.loadFile(category)
        self.wrong_guesses_allowed = wrong_guesses_allowed #number of times player can guess the letters for each word
        self.start_game()
   
    def start_game(self):  
        #word for player to guess
        self.selected_word = self.pick_word() 
        #return false if there is no more word left
        if(self.selected_word == None): 
            return False
        #word player is guessing so far
        self.display_letters = self.init_letters() 
        #list of letters playered wrongly guessed
        self.wrong_letters = [] 
        #number of letters player is guessing wrongly
        self.wrong_guesses = 0 
        self.hint_limit = 2
        #list to keep hint letters
        self.hint_list = [i for i in self.selected_word] 
        return True
    
    def pick_word(self):
        #check if there is any word left to play
        remaining = len(self.word_list)
        if(remaining > 0):
            word = random.choice(self.word_list)
            print('-----------------------------------------------')
            print('Selected word: ', word)
            
            #remove the selected word from the list
            self.word_list.remove(word)
            print('Remaining words: ', len(self.word_list))
        
            return word
        return None
        
    def init_letters(self):
        #represent each letter in the word as '_'
        letters = ['_'] * len(self.selected_word)
        return letters
        
    def loadFile(self, category):
        #directory of word text files
        word_dir = 'words/'
        with open(word_dir+category+'.txt', 'r') as file:
            word_list = file.read().splitlines()
        return word_list
    
    def guess_letter(self, letter):
        indices = [i for i, 
                   char in enumerate(self.selected_word) 
                   if char == letter]
        is_correct = True
        if(len(indices) == 0):
            self.wrong_letters.append(letter)
            self.wrong_guesses += 1
            is_correct = False
        else:
            for i in indices:
                self.display_letters[i] = self.selected_word[i]
        
        #remove guessed letter or hint from hint_list
        self.remove_letter_from_hint_list(letter)
        
        return is_correct
        
    def check_win(self):
        #player has guessed the word correctly if there is no "_" in list
        if not '_' in self.display_letters:
            HangMan.score += 1
            return True
        return False
    
    def check_lose(self):
        return self.wrong_guesses >= self.wrong_guesses_allowed
    
    def display_word(self):
        display_word = " ".join(self.display_letters)
        return display_word.upper()
        
    def display_wrong_letters(self):
        display_wrong_letters = ", ".join(self.wrong_letters)
        return display_wrong_letters.upper()
        
    def display_hint_limit(self):
        display_hint_limit = str(self.hint_limit) + "/2 left"
        return display_hint_limit
        
    def get_hint(self):
        hint = random.choice(self.hint_list)
        
        #reduce hint_limit by 1
        self.hint_limit = self.hint_limit - 1
        return hint
        
    def remove_letter_from_hint_list(self, letter):
        self.hint_list = list(filter(lambda x: x != letter, 
                                     self.hint_list))
        

        
        
        
        
        