from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUiType

from hangman import HangMan
from functools import partial

import os
import sys
import time


class ThreadProgress(QThread):
    mysignal = pyqtSignal(int)
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
    def run(self):
        i = 0
        while i<11:
            time.sleep(0.06)
            self.mysignal.emit(i)
            i += 1

FROM_SPLASH,_ = loadUiType(os.path.join(os.path.dirname(__file__),"splash.ui"))
FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"main.ui"))
FROM_HANGMAN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"hangman_test.ui"))

class HangManTest(QMainWindow, FROM_HANGMAN):
    def __init__(self, parent=None):
        super(HangManTest, self).__init__(parent)
        self.setupUi(self)
        self.hangman = HangMan(selected_category)
        self.prepare_screen()
        #map the clicked button from UI to respective category
        buttons = {self.btn_a : 'a', self.btn_b : 'b', self.btn_c : 'c'}
        for  button in  buttons:
            button.clicked.connect(partial(self.select_letter, buttons[button]))
        self.btn_next.clicked.connect(self.play_next)
        
    def prepare_screen(self):
        self.lbl_wrong_letters.setText(self.hangman.display_wrong_letters())
        self.lbl_word.setText(self.hangman.display_word())
        self.lbl_score.setText(str(self.hangman.score))
        
    def select_letter(self, letter):
        #initialize hangman instance
        self.hangman.guess_letter(letter)
        self.prepare_screen()
    
    def play_next(self):
        self.hangman.start_game()
        self.prepare_screen()
        
class Main(QMainWindow, FROM_MAIN):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        
        #map the clicked button from UI to respective category
        buttons = {self.btn_fruits : 'fruits', self.btn_animals : 'animals', self.btn_sports : 'sports'}
        for  button in  buttons:
            button.clicked.connect(partial(self.select_category, buttons[button]))
        
    def select_category(self, category):
        QMessageBox.information(self, "Hangman", category.capitalize() + " category has been selected!")
        #----------------------------------------------------------------------
        global selected_category 
        selected_category = category
        self.hide()
        hmt = HangManTest(self)
        hmt.show()    

        
class Splash(QMainWindow, FROM_SPLASH):
    def __init__(self, parent = None):
        super(Splash, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        pixmap = QPixmap("splash.jpg")
        self.splah_image.setPixmap(pixmap.scaled(1200, 750))
        progress = ThreadProgress(self)
        progress.mysignal.connect(self.progress)
        progress.start()
        
    @pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i)
        if i == 10:
            self.hide()
            main = Main(self)
            main.show()


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