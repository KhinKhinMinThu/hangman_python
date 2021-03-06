from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton
from PyQt5.QtGui import QPixmap, QFont
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
        while i<101:
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
        if i == 100:
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
        global selected_category 
        selected_category = category
        #add menu selection sound
        beep_sound.play()
        time.sleep(1)
        beep_sound.stop()
        self.hide()
        hmt = HangmanGame(self)
        hmt.show()    


class HangmanGame(QMainWindow, FROM_HANGMAN):
    def __init__(self, parent=None):
        super(HangmanGame, self).__init__(parent)
        #set up UI from the self object
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
            self.play_sound(correct_sound, 0.5)
        else:
            self.play_sound(error_sound, 0.5)
            self.image_index += 1;
            self.refresh_image()

        self.prepare_screen()
        self.check_result()
        
    def play_sound(self, sound, sec):
        sound.play()
        time.sleep(sec)
        sound.stop()
        
    def generate_hint(self):
        # disable the hint button, if the hint limitation is reached
        if  self.hangman.hint_limit == 0:
            sender = self.sender()
            sender.setEnabled(False)
            
        else:
            hint = self.hangman.get_hint()
            self.hangman.guess_letter(hint)
            self.play_sound(correct_sound, 0.5)
            #disable the hinted alphabet button
            for button in self.buttons:
                if self.buttons.get(button) == hint:
                    button.setEnabled(False)
            self.prepare_screen()
            self.check_result()
              
    def play_next(self):
        is_valid = self.hangman.start_game()
        if(is_valid == False): #no more word left to play
            self.close() #close the application
        else:
            self.play_sound(beep_sound, 0.5)
            self.activate_all()
            self.image_index = 0
            self.refresh_image()
            self.prepare_screen()

    def prepare_screen(self):
        #initial set up to display respective label on screen
        self.lbl_wrong_letters.setText("Missed Letters: " + self.hangman.display_wrong_letters())
        self.lbl_category.setText("Category: " + selected_category.capitalize())
        self.lbl_word.setText(self.hangman.display_word())
        self.lbl_score.setText("Total Score: " + str(self.hangman.score))
        self.lbl_hint.setText(self.hangman.display_hint_limit())
        
    def activate_all(self):
        for button in self.buttons:
            button.setEnabled(True)
        self.btn_hint.setEnabled(True)

    def check_result(self):    
        is_win = self.hangman.check_win()
        is_lose = self.hangman.check_lose()
    
        msg_box = QMessageBox(self)
        font = QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(12)
        
        btn_next = QPushButton('Next')
        btn_close = QPushButton('Close')
        btn_again = QPushButton('Play Again')
        btn_next.setFont(font)
        btn_close.setFont(font)
        btn_again.setFont(font)

        
        if(is_win):
            msg_box.setIconPixmap(QPixmap("image/win.png"))
            msg_box.setText("Congratulations you just won!\n\nClick \"Next\" to continue.")
            msg_box.addButton(btn_next, QMessageBox.YesRole)
            self.play_sound(success_sound, 1.2)
                        
        if(is_lose):
            msg_box.setIconPixmap(QPixmap("image/lose.png"));
            msg_box.setText("Sorry, you just lost the game.\n\nCorrect Word: " + self.hangman.selected_word.upper() + "\n\nTotal Score: " + str(self.hangman.score))
            msg_box.addButton(btn_again, QMessageBox.YesRole)
            self.play_sound(gameover_sound, 1.2)
        
        if(is_win | is_lose):
            msg_box.setWindowTitle("Game Result")
            msg_box.addButton(btn_close, QMessageBox.NoRole)
            msg_box.buttonClicked.connect(self.result_action)
            
            msg_box.setBaseSize(QSize(1000, 120));
            
            msg_box.setFont(font)
            msg_box.exec_()
            
    def result_action(self, btn):
        if(btn.text() == 'Next'):
            self.play_next()
        elif(btn.text() == 'Play Again'):
            self.hide()
            category = Category(self)
            category.show()
            HangMan.score = 0
        else:
            #close the application
            self.close()
            
global main
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