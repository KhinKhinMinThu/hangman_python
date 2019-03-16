from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUiType

from HangMan import HangMan
from functools import partial

import os
import sys
import time

FROM_SPLASH,_ = loadUiType(os.path.join(os.path.dirname(__file__),"splash.ui"))
FROM_CATEGORY,_ = loadUiType(os.path.join(os.path.dirname(__file__),"category.ui"))
FROM_HANGMAN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"hangman.ui"))


# Progress bar
class ThreadProgress(QThread):
    mysignal = pyqtSignal(int)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def run(self):
        i = 0
        #To change to 101
        while i<51:
            time.sleep(0.06)
            self.mysignal.emit(i)
            i += 1


# Splash Screen        
class Splash(QMainWindow, FROM_SPLASH):
    def __init__(self, parent = None):
        super(Splash, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        pixmap = QPixmap("image/splash.jpg")
        self.splah_image.setPixmap(pixmap.scaled(1200, 750))
        progress = ThreadProgress(self)
        progress.mysignal.connect(self.progress)
        progress.start()
        
    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        #To change to 100
        if i == 50:
            self.hide()
            category = Category(self)
            category.show()

# Category Selection Screen
class Category(QMainWindow, FROM_CATEGORY):
    def __init__(self, parent=None):
        super(Category, self).__init__(parent)
        self.setupUi(self)
        
        #map the clicked button from UI to respective category
        buttons = {self.btn_fruits : 'fruits', self.btn_animals : 'animals', self.btn_sports : 'sports'}
        for  button in  buttons:
            button.clicked.connect(partial(self.select_category, buttons[button]))
        
    def select_category(self, category):
        #QMessageBox.information(self, "Hangman", category.capitalize() + " category has been selected!")
        #----------------------------------------------------------------------
        global selected_category 
        selected_category = category
        self.hide()
        hmt = HangmanGame(self)
        hmt.show()    


class HangmanGame(QMainWindow, FROM_HANGMAN):
    def __init__(self, parent=None):
        super(HangmanGame, self).__init__(parent)
        self.setupUi(self)
        #initialize hangman instance with selected category
        self.hangman = HangMan(selected_category)
        self.prepare_screen()
        #map the clicked button from UI to respective letter 
        buttons = {self.btn_a : 'a', self.btn_b : 'b', self.btn_c : 'c', self.btn_d: 'd', self.btn_e: 'e', self.btn_f: 'f',
                self.btn_g : 'g', self.btn_h : 'h', self.btn_i : 'i', self.btn_j: 'j', self.btn_k: 'k', self.btn_l: 'l',
                self.btn_m : 'm', self.btn_n : 'n', self.btn_o : 'o', self.btn_p: 'p', self.btn_q: 'q', self.btn_r: 'r',
                self.btn_s : 's', self.btn_t : 't', self.btn_u : 'u', self.btn_v: 'v', self.btn_w: 'w', self.btn_x: 'x',
                self.btn_y : 'y', self.btn_z : 'z'}

        for  button in  buttons:
            button.clicked.connect(partial(self.select_letter, buttons[button]))

        #To reset the buttons => so need to instance object's attribute
        self.buttons = buttons; 

        #Player guessed the word correctly and move on to next game
        #Next button is disabled until the player wins
        self.btn_next.setEnabled(False)
        self.btn_next.clicked.connect(self.play_next)

        self.frames_image_list = ['image/1.png','image/2.png','3.png','4.png','5.png','6.png'];

        pixmap = QPixmap(self.frames_image_list[0])
        self.image_lbl_1.setPixmap(pixmap);
        
    def select_letter(self, letter):
        # disable the button
        sender = self.sender()
        sender.setEnabled(False)
        
        self.hangman.guess_letter(letter)
        self.prepare_screen()
        self.check_result()
        
    def play_next(self):
        self.hangman.start_game()
        self.activate_all()
        self.prepare_screen()

    def prepare_screen(self):
        self.lbl_wrong_letters.setText(self.hangman.display_wrong_letters())
        self.lbl_word.setText(self.hangman.display_word())
        self.lbl_score.setText(str(self.hangman.score))
        
    def activate_all(self):
        for button in self.buttons:
            button.setEnabled(True)
        self.btn_next.setEnabled(False)

    def check_result(self):    
        message = img = ''
        is_display = False
        
        if(self.hangman.check_win()):
            message = 'You Win!'
            img = "image/win.png"
            self.btn_next.setEnabled(True)
            is_display = True
            
        if(self.hangman.check_lose()):
            message = 'You Lose!'
            img = "image/lose.png"
            is_display = True
    
        if(is_display):     
            msg = QMessageBox(self)
            msg.setIconPixmap(QPixmap(img));
            msg.setText(message)
            msg.setWindowTitle("Game Result")
            msg.exec_()
        

def main():
    app=QApplication(sys.argv)
    window = Splash()
    window.show()
    app.exec_()

if __name__ == '__main__':
    try:
        main()
    except Exception as why:
        print(why)