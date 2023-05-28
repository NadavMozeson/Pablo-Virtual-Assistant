import speech_recognition as sr
from pabloGUI import openGui, create_icon

def heyPablo():

    def command():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            print("Listening...")
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say that again please...")
            return "None"
        return query

    while True:
        query = command().lower()
        if 'hey pablo' in query or 'hello pablo' in query:
            openGui()

if __name__ == '__main__':
    #heyPablo()
    create_icon()
