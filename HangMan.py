# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 14:57:31 2019

@author: Khin Khin Min Thu
"""
import random

class HangMan:
    pics = ["1.png", "2.png", "3.png", "4.png", "5.png", "6.png"]
    word_lists = {}
    
    def __init__(self):
        self.selected_word = '' #word for player to guess
        self.correct_alpha = [] #word player is guessing so far
        self.wrong_alpha = [] #list of letter playered wrongly guessed
        self.win = False #True is player can guess the whole word correctly
    
    def select_category(self, category):
        #load the words for selected category if it hasn't done so
        is_exist = self.word_lists.get(category, 0)
        if(is_exist == 0):
            self.word_lists[category] = self.loadFiles(category)
            
        print('Total loaded categories: ', len(self.word_lists))
        
        #choose a random word for the list
        word_list = self.word_lists[category]
        self.selected_word = random.choice(word_list)
        print('Selected word: ', self.selected_word, ', Len: ', len(self.selected_word))
        
        #initialize the correct alphabets with None
        self.correct_alpha = [None] * len(self.selected_word)
        
        #remove the selected word from the list
        word_list.remove(self.selected_word)
        print('Removed word: ', self.selected_word, ', Remaining words for ('+category+'): ', len(self.word_lists[category]))
        print('-------------------------------------------------------------------')
        
        
    def loadFiles(self, category):
        word_dir = 'words/'
        with open(word_dir+category+'.txt', 'r') as file:
            word_list = file.read().splitlines()
            
        #print('Total words loaded ('+category+'): ', len(word_list))
        return word_list
    
    def guess_alpha(self, alpha):
        #return the list of indices for the alphabet in selected word
        #e.g., word='mayapple', alpha='a' --> index = [1, 3]
        #e.g., word='cougar', alpha='a' --> index = [4]
        indices = [i for i, char in enumerate(self.selected_word) if char == alpha]
        
        if(len(indices) == 0):
            self.wrong_alpha.append(alpha)
            
        else:
            for i in indices:
                self.correct_alpha[i] = self.selected_word[i]
        
        #player has guessed the word correctly if there is no "None" in the list
        if not None in self.correct_alpha == False:
            self.win = True
            
        print('Guessed alpha: ', alpha)
        print('Wrongly guessed alpha: ', self.wrong_alpha)
        print('Correct alphas so far: ', self.correct_alpha)
        print('Did player win?: ', self.win)
        print('-------------------------------------------------------------------')
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        