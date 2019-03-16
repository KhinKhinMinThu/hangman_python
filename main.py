from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUiType
from pygame import mixer
#py -3.7 -m pip install pygame (run this command for pygame installation)
from HangMan import HangMan
from functools import partial

import os
import sys
import time

FROM_SPLASH,_ = loadUiType(os.path.join(os.path.dirname(__file__),"splash.ui"))
FROM_CATEGORY,_ = loadUiType(os.path.join(os.path.dirname(__file__),"category.ui"))
FROM_HANGMAN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"hangman.ui"))

mixer.init()
correct_sound = mixer.Sound("sound/correct.wav")
error_sound = mixer.Sound("sound/error.wav")
success_sound = mixer.Sound("sound/success.wav")
beep_sound = mixer.Sound("sound/beep.wav")
gameover_sound = mixer.Sound("sound/gameover.wav")
gamestart_sound = mixer.Sound("sound/gamestart.wav")

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
        gamestart_sound.play()
        #To change to 100
        if i == 50:
            gamestart_sound.stop()
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
        #----------------------------------------------------------------------
        global selected_category 
        selected_category = category
        #add menu selection sound
        beep_sound.play()
        time.sleep(2)
        beep_sound.stop()
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
        
        #Hint Button
        #hint_limit = 2
        self.btn_hint.clicked.connect(self.generate_hint)

        self.frames_image_list = ['image/1.jpg','image/2.jpg','image/3.jpg','image/4.jpg','image/5.jpg','image/6.jpg','image/7.jpg'];
        self.image_index = 0
        self.refresh_image()
    
    def refresh_image(self):
        pixmap = QPixmap(self.frames_image_list[self.image_index])
        self.image_lbl_1.setPixmap(pixmap)
      
    def select_letter(self, letter):
        # disable the button
        sender = self.sender()
        sender.setEnabled(False)
        is_correct = self.hangman.guess_letter(letter)
        #add sound effects
        if is_correct:
            self.play_sound(correct_sound)
        else:
            self.play_sound(error_sound)
            self.image_index += 1;
            self.refresh_image()


        self.prepare_screen()
        self.check_result()
        
    def play_sound(self, sound):
        sound.play()
        time.sleep(0.1)
        sound.stop()
        
    def generate_hint(self):
        # disable the hint button, if the hint limitation is reached
        if  self.hangman.hint_limit == 0:
            sender = self.sender()
            sender.setEnabled(False)
            
        else:
            hint = self.hangman.get_hint()
            self.hangman.guess_letter(hint)
            self.play_sound(correct_sound)
            #disable the hinted alphabet button
            for button in self.buttons:
                if self.buttons.get(button) == hint:
                    button.setEnabled(False)
            self.prepare_screen()
            self.check_result()
              
    def play_next(self):

        self.play_sound(beep_sound)
        self.hangman.start_game()
        self.activate_all()
        self.image_index = 0
        self.refresh_image()
        self.prepare_screen()

    def prepare_screen(self):
        self.lbl_wrong_letters.setText(self.hangman.display_wrong_letters())
        self.lbl_word.setText(self.hangman.display_word())
        self.lbl_score.setText(str(self.hangman.score))
        self.lbl_hint.setText(self.hangman.display_hint())
        
    def activate_all(self):
        for button in self.buttons:
            button.setEnabled(True)
        self.btn_next.setEnabled(False)
        self.btn_hint.setEnabled(True)

    def check_result(self):    
        message = img = ''
        is_display = False
        
        if(self.hangman.check_win()):
            message = 'You Win!'
            img = "image/win.png"
            self.btn_next.setEnabled(True)
            is_display = True
            self.play_sound(success_sound)
            
        if(self.hangman.check_lose()):
            message = 'You Lose!'
            img = "image/lose.png"
            is_display = True
            self.play_sound(gameover_sound)
    
        if(is_display):     
            msg = QMessageBox(self)
            msg.setIconPixmap(QPixmap(img));
            msg.setText(message)
            msg.setWindowTitle("Game Result")
            msg.exec_()
            # QCoreApplication.instance().quit()
        

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