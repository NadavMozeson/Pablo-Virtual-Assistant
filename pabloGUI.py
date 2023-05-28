import tkinter as tk
from PIL import Image
import pystray
import threading
import speech_recognition as sr
import pyttsx3
import sys

engine = pyttsx3.init()
root = None
icon = None
open_event = threading.Event()
exit_event = threading.Event()

def on_open(item):
    if root:
        root.deiconify()
    else:
        openGui()

def on_exit(icon, item):
    icon.stop()
    exit_event.set()
    if root:
        root.quit()

def openGui():
    global root

    def listen():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-IN')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()
    button = tk.Button(frame, text="LISTEN", fg="red", command=listen)
    button.pack(side=tk.LEFT)

    root.protocol('WM_DELETE_WINDOW', root.destroy)
    root.bind("<FocusOut>", lambda event: root.destroy())
    root.overrideredirect(True)

    while True:
        try:
            root.update()
        except tk.TclError:
            break

        if open_event.is_set():
            root.deiconify()
            open_event.clear()

        if exit_event.is_set():
            break

        root.after(100)

def create_icon():
    global icon
    image = Image.open("logo.png")
    menu = (
        pystray.MenuItem('Talk to Pablo', on_open),
        pystray.MenuItem('Quit', on_exit),
    )
    icon = pystray.Icon("name", image, "Pablo", menu)
    icon.run()
