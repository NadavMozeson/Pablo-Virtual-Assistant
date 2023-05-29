import tkinter as tk
import pystray
import threading
import speech_recognition as sr
import pyttsx3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTextEdit, QLineEdit, QPushButton, QLabel
from engine import preform
from loadConfig import load_config
from PIL import ImageTk, Image

engine = pyttsx3.init()
root = None
icon = None
app = None
open_event = threading.Event()
exit_event = threading.Event()
config = load_config()

def on_open(item):
    if root:
        if root and root.isVisible():
            root.hide()
        else:
            root.show()
    else:
        openGui()

def on_exit(icon, item):
    icon.stop()
    exit_event.set()
    if root:
        root.close()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-IN')
        print(f"User said: {query}\n")
        preform(query)
    except Exception as e:
        print("Say that again please...")

def listen_thread(event):
    threading.Thread(target=listen).start()

def speak(audio):
    config = load_config()
    if config['voice-on']:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[config['voice']].id)
        engine.say(audio)
        engine.runAndWait()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, temp_app):
        super().__init__()
        self.app = temp_app
        self.guiElements()

    def guiElements(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.SplashScreen)
        self.setGeometry(100, 100, 300, 600)
        self.setWindowTitle("Pablo - Personal Assistant Bot")

        # Configure the style settings
        self.app.setStyle("Fusion")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#3d5e6f"))
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor("#ffc579"))
        palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor("#31323f"))
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#3b5667"))
        palette.setColor(QtGui.QPalette.Text, QtGui.QColor("#dadae2"))
        self.app.setPalette(palette)

        # Create the widgets
        frame = QtWidgets.QWidget(self)
        frame.setObjectName("frame")
        self.setCentralWidget(frame)
        layout = QtWidgets.QGridLayout(frame)
        history = QTextEdit(frame)
        history.setReadOnly(True)
        entry = QLineEdit(frame)
        entry.setPlaceholderText("Send a message to Pablo...")
        entry.setStyleSheet("""
            QLineEdit {
                color: #dadae2;
            }
            QLineEdit::placeholder {
                color: #708494;
            }
        """)
        send_button = QPushButton("Send", frame)
        image = QtGui.QImage("logo.png")
        image = image.scaled(100, 100, QtCore.Qt.KeepAspectRatio)
        photo = QtGui.QPixmap.fromImage(image)
        listen_button = QLabel(frame)
        listen_button.setPixmap(photo)

        # Add the widgets to the layout
        layout.addWidget(history, 0, 0, 1, 2)
        layout.addWidget(entry, 1, 0)
        layout.addWidget(send_button, 1, 1)
        layout.addWidget(listen_button, 2, 0, 1, 2)

        screen_geometry = self.app.desktop().availableGeometry()
        root_geometry = self.geometry()
        x = screen_geometry.width() - root_geometry.width()
        self.move(x, 0)

    def closeEvent(self, event):
        if not exit_event.is_set():
            event.ignore()
            self.hide()
        else:
            event.accept()

    def event(self, event):
        if event.type() == QtCore.QEvent.WindowDeactivate:
            self.hide()
        return super().event(event)

def openGui():
    global root, app

    app = QtWidgets.QApplication(sys.argv)

    root = MainWindow(app)
    root.show()
    sys.exit(app.exec_())

def create_icon():
    global icon
    image = Image.open("logo.png")
    menu = (
        pystray.MenuItem('Talk to Pablo', on_open),
        pystray.MenuItem('Quit', on_exit),
    )
    icon = pystray.Icon("name", image, "Pablo", menu)
    icon.run()
