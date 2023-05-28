import webbrowser as wb
import pyttsx3
from loadConfig import load_config, update_config
import urllib.parse

engine = pyttsx3.init()

def preform(str):
    config = load_config()
    websites = eval(config["websites"])
    if "open" in str.lower():
        for i in websites.keys():
            if f"open {i}" in str.lower():
                wb.open_new_tab(websites[i])
                speak(f"opening {i}")
                break
    elif "google search" in str.lower():
        wb.open_new_tab(f"https://www.google.com/search?q={urllib.parse.quote(str.lower().split('google search')[1])}")
        speak(f"searching {str.lower().split('google search')[1]}")
    elif "call me" in str.lower():
        update_config("name", str.lower().split('call me ')[1])
        config = load_config()
        speak(f"I will call you {config['name']} from now on")
    elif "change voice" in str.lower():
        update_config("voice", not config["voice"])
        speak("voice changed")
    elif "disable voice" in str.lower() or "enable voice" in str.lower():
        update_config('voice-on', not config['voice-on'])
        speak("voice turned on")

def speak(audio):
    config = load_config()
    if config['voice-on']:
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[config['voice']].id)
        engine.say(audio)
        engine.runAndWait()
