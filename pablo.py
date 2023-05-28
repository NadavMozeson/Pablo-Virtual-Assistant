import json
import tkinter as tk
import speech_recognition as sr
import pyttsx3

with open('config.json') as f:
    config = json.load(f)

engine = pyttsx3.init()

def openGui():
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

    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[config["voice"]].id)
    speak(f"Hello {config['name']}")
    root.mainloop()
