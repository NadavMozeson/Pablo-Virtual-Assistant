import webbrowser as wb
from loadConfig import load_config, update_config
import urllib.parse

def preform(str):
    config = load_config()
    websites = eval(config["websites"])
    if "open" in str.lower():
        for i in websites.keys():
            if f"open {i}" in str.lower():
                wb.open_new_tab(websites[i])
    elif "google search" in str.lower():
        wb.open_new_tab(f"https://www.google.com/search?q={urllib.parse.quote(str.lower().split('google search')[1])}")
    elif "call me" in str.lower():
        update_config("name", str.lower().split('call me ')[1])
