# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:57:31 2019

@author: Khin Khin Min Thu
"""
import random

class HangMan:
    #static class variable to keep the score throughout the games while game instances reset
    score = 0    
    def __init__(self, category, allowed_guesses=6):
        self.word_list = self.loadFile(category)
        self.allowed_guesses = allowed_guesses #number of times player can guess the letters for each word
        self.start_game()
   
    def start_game(self):     
        self.selected_word = self.pick_word() #word for player to guess
        if(self.selected_word == None): #return false if there is no more word left
            return False
        self.display_letters = self.init_letters() #word player is guessing so far
        self.wrong_letters = [] #list of letters playered wrongly guessed
        self.wrong_guesses = 0 #number of letters player is guessing wrongly
        self.hint_limit = 2
        #dictionary of hints -> letter as Value and indices as Key
        indices_keys = [i for i in range(len(self.selected_word))]
        self.hint_dict = {key: self.selected_word[key] for key in indices_keys}
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
        #initialize the list with '_'
        letters = ['_'] * len(self.selected_word)
        return letters
        
    def loadFile(self, category):
        word_dir = 'words/'
        with open(word_dir+category+'.txt', 'r') as file:
            word_list = file.read().splitlines()
        return word_list
    
    def guess_letter(self, letter):
        indices = [i for i, char in enumerate(self.selected_word) if char == letter]
        is_correct = True
        if(len(indices) == 0):
            self.wrong_letters.append(letter)
            self.wrong_guesses += 1
            is_correct = False
        else:
            for i in indices:
                self.display_letters[i] = self.selected_word[i]
        
        #remove guessed letter from hint_dict
        self.remove_letter_from_hint(letter)
        
        return is_correct
        
    def check_win(self):
        #player has guessed the word correctly if there is no "_" in the list
        if not '_' in self.display_letters:
            HangMan.score += 1
            return True
        return False
    
    def check_lose(self):
        return self.wrong_guesses >= self.allowed_guesses
    
    def display_word(self):
        display_word = " ".join(self.display_letters)
        return display_word.upper()
        
    def display_wrong_letters(self):
        display_wrong_letters = ", ".join(self.wrong_letters)
        return display_wrong_letters.upper()
        
    def display_hint(self):
        display_hint = str(self.hint_limit) + "/2 left"
        return display_hint
        
    def get_hint(self):
        hints = list(self.hint_dict.values())
        hint = random.choice(hints)
        print('hints', hints)
        print('Selected hint: ', hint)
        
        #remove the selected hint from the list
        self.remove_letter_from_hint(hint)
        
        #reduce hint_limit by 1
        self.hint_limit = self.hint_limit - 1
       
        print('Removed hint: ', hint, ', Remaining hints: ', self.hint_dict)
        return hint
        
    def remove_letter_from_hint(self, letter):
        to_remove = []
        #loop hint dictionary
        for key in self.hint_dict.keys():
            #for each key in hint_dict, if the key's value is same as letter, remove that letter from hint_dict
            if self.hint_dict.get(key) == letter:
                to_remove.append(key)  
        
        for i in to_remove:
            self.hint_dict.pop(i, None)
        
        
        
        
        
        
        