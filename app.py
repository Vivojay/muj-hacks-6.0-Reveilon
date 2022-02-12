import os
import sys
import time
import playsound
import subprocess as sp

# Spawn the Sign Language Recognition Module
sp.Popen(["py", "SignLanguage_new.py"], shell=True)

from gtts import gTTS

# cd to Working Directory
cur_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(cur_dir)

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QSlider,
    QFileDialog,
    QStyle,
    QStyleOptionSlider,
)

from PyQt5.QtGui import (
    QIcon,
    QPixmap
)

from PyQt5.QtCore import (
    pyqtSlot,
    QTimer,
    QSize,
    QRect,
    Qt
)

with open("styles/slider_style.qss") as file:
    seekslider_stylesheet = file.read()

class functions:
    def Speak(mytext):
        global speechSoundFile
        speechSoundFile = 'temp'
        language = 'en-US'

        if os.path.exists(os.path.join(os.path.dirname(__file__), speechSoundFile+'.mp3')):
            os.remove(os.path.join(os.path.dirname(__file__), speechSoundFile+'.mp3'))
        myobj = gTTS(text=mytext, lang=language, slow=False)
        myobj.save(speechSoundFile+".mp3")

        print(os.path.join(os.path.dirname(__file__), speechSoundFile+'.mp3'))
        playsound.playsound(os.path.join(os.path.dirname(__file__), speechSoundFile+'.mp3'))

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "s1gnia"
        self.left = 10
        self.top = 100
        self.width = 320
        self.height = 200

        self.initUI()

        self.letter_display = QLabel(self)
        self.letter_display.setText("")
        self.letter_display.setStyleSheet("color: white; font-size: 50px;")

        self.setWindowIcon(QIcon("resources/icons/master.svg"))
        self.setStyleSheet(
            # background-image: url(:resources/images/master_bg.jpg);
            """
            background: #212121;
            border: none;
            """
        )

        self.letterUpdate()

        self.show()

    def letterRead(self):
        with open('letter', 'r', encoding='utf-8') as fp:
            return fp.read().strip()

    def letterUpdate(self):
        self.letter_display.setText(self.letterRead().lower())

        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.letterUpdate)
        self.timer.start(1000)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.button = QPushButton("", self)
        # self.button.setToolTip("Toggle Play/Pause")
        # self.button.move(110, 70)
        # self.button.clicked.connect(self.letterUpdate)

        # self.button.setIcon(QIcon(rf"D:\OneDrive - Suncity School\My Stuff\-COMPUTERS-\My Py Files\SIGN-LANG-MUJ-HACK-6.0\AI Volume Control\venv\Lib\site-packages\matplotlib\mpl-data\images\home.svg"))
        # self.button.setIconSize(QSize(40, 40))
        # # self.button.setStyleSheet(f'background-image: url(resources/Layouts/{Layout}/MediaControls/play.svg);')
        # self.button.resize(200, 200)


if __name__ == "__main__":
    # --- Start App --- #
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()

    # multi()
