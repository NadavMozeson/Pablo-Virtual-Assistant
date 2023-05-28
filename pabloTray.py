import tkinter as tk
from PIL import Image
import pystray
import threading
import speech_recognition as sr
import pyttsx3
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

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

def minimize_window(event):
    root.withdraw()

def unmap_window(event):
    root.iconify()

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

    def send_message():
        message = entry.get()
        # Process the message here
        print(message)
        entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Pablo - Personal Assistant Bot")
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    history = ScrolledText(frame, width=30, height=10, wrap=tk.WORD)
    history.grid(column=0, row=0, columnspan=2, sticky=(tk.W, tk.E))
    history.config(state='disabled')
    entry = ttk.Entry(frame, width=20)
    entry.grid(column=0, row=1, sticky=(tk.W, tk.E))
    send_button = ttk.Button(frame, text="Send", command=send_message)
    send_button.grid(column=1, row=1, sticky=tk.W)
    listen_button = ttk.Button(frame, text="Listen", command=listen)
    listen_button.grid(column=0, row=2, columnspan=2)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=3)
    frame.columnconfigure(1, weight=1)

    root.protocol('WM_DELETE_WINDOW', root.withdraw)
    root.geometry("+{}+{}".format(root.winfo_screenwidth() - root.winfo_reqwidth()-90, 0))
    root.mainloop()

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
