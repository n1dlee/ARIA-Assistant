import tkinter as tk
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import threading
import logging
from PIL import Image, ImageTk

def setup_logging():
    logging.basicConfig(filename='voice_assistant.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def log_response(response):
    logging.info(response)
    console_log.config(state=tk.NORMAL)  # Enable writing to the console log
    console_log.insert(tk.END, response + '\n')
    console_log.config(state=tk.DISABLED)  # Disable writing to the console log

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        console_log.config(state=tk.NORMAL)  # Enable writing to the console log
        console_log.insert(tk.END, "Listening...\n")
        console_log.config(state=tk.DISABLED)  # Disable writing to the console log
        audio = recognizer.listen(source)

    try:
        console_log.config(state=tk.NORMAL)  # Enable writing to the console log
        console_log.insert(tk.END, "Recognizing...\n")
        console_log.config(state=tk.DISABLED)  # Disable writing to the console log
        query = recognizer.recognize_google(audio)
        console_log.config(state=tk.NORMAL)  # Enable writing to the console log
        console_log.insert(tk.END, "You said: " + query + '\n')
        console_log.config(state=tk.DISABLED)  # Disable writing to the console log
        return query.lower()
    except sr.UnknownValueError:
        console_log.config(state=tk.NORMAL)  # Enable writing to the console log
        console_log.insert(tk.END, "Sorry, I couldn't understand what you said.\n")
        console_log.config(state=tk.DISABLED)  # Disable writing to the console log
        return ""
    except sr.RequestError:
        console_log.config(state=tk.NORMAL)  # Enable writing to the console log
        console_log.insert(tk.END, "Sorry, there was an issue with the speech recognition service.\n")
        console_log.config(state=tk.DISABLED)  # Disable writing to the console log
        return ""

def open_program(program_name):
    try:
        os.startfile(program_name)
    except Exception as e:
        console_log.config(state=tk.NORMAL)  # Enable writing to the console log
        console_log.insert(tk.END, str(e) + '\n')
        console_log.config(state=tk.DISABLED)  # Disable writing to the console log
        speak("Sorry, I couldn't open the program.")

def open_website(website_url):
    try:
        webbrowser.open(website_url)
    except Exception as e:
        console_log.config(state=tk.NORMAL)  # Enable writing to the console log
        console_log.insert(tk.END, str(e) + '\n')
        console_log.config(state=tk.DISABLED)  # Disable writing to the console log
        speak("Sorry, I couldn't open the website.")

def play_music_on_youtube(song_name):
    query = song_name.replace(" ", "+")
    url = f"https://www.youtube.com/results?search_query={query}"
    open_website(url)

def stop_voice_assistant():
    console_log.config(state=tk.NORMAL)  # Enable writing to the console log
    console_log.insert(tk.END, "Assistant stopped.\n")
    console_log.config(state=tk.DISABLED)  # Disable writing to the console log

def leave_assistant():
    console_log.config(state=tk.NORMAL)  # Enable writing to the console log
    console_log.insert(tk.END, "Assistant is leaving. Goodbye!\n")
    console_log.config(state=tk.DISABLED)  # Disable writing to the console log
    root.destroy()

def start_voice_assistant():
    console_log.config(state=tk.NORMAL)  # Enable writing to the console log
    console_log.insert(tk.END, "Hello! How can I assist you?\n")
    console_log.config(state=tk.DISABLED)  # Disable writing to the console log
    while True:
        query = listen()
        log_response(query)

        if "chrome" in query:
            open_program("chrome.exe")
        elif "youtube" in query:
            open_website("https://www.youtube.com")
        elif "spotify" in query:
            open_program("spotify.exe")
        elif "steam" in query:
            open_program("steam.exe")
        elif "calculator" in query:
            open_program("calc.exe")
        elif "this computer" in query:
            open_program("explorer.exe")
        elif "open website" in query:
            speak("Sure, which website would you like to open?")
            website_query = listen()
            log_response(website_query)
            if website_query:
                open_website("https://" + website_query)
        elif "play music" in query:
            speak("Sure, what song would you like to listen to?")
            song_query = listen()
            log_response(song_query)
            if song_query:
                play_music_on_youtube(song_query)
        elif "open video" in query:
            speak("Sure, what video would you like to watch to?")
            song_query = listen()
            log_response(song_query)
            if song_query:
                play_music_on_youtube(song_query)
        elif "stop assistant" in query:
            stop_voice_assistant()
            break
        elif "leave assistant" in query:
            leave_assistant()
            break
        else:
            speak("Sorry, I don't understand that command.")
            log_response("Unknown command: " + query)

def main():
    global root
    root = tk.Tk()
    root.title("Voice Assistant")
    root.geometry("600x480")

    setup_logging()

    # Create a console log inside the application
    global console_log
    console_log = tk.Text(root, bg="black", fg="white", wrap=tk.WORD, state=tk.DISABLED)
    console_log.pack(fill=tk.BOTH, expand=True)

    # Load the background image
    background_image = Image.open("bgfile\wallground.jpg")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a label to display the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Create the "Start Assistant" button
    def start_voice_assistant_thread():
        threading.Thread(target=start_voice_assistant).start()

    button = tk.Button(root, text="Start Assistant", command=start_voice_assistant_thread)
    button.pack(pady=10)

    # Create the "Stop Assistant" button
    stop_button = tk.Button(root, text="Stop Assistant", command=stop_voice_assistant)
    stop_button.pack(pady=5)

    # Create the "Leave Assistant" button
    leave_button = tk.Button(root, text="Leave Assistant", command=leave_assistant)
    leave_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
