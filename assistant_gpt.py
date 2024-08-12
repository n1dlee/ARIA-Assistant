import tkinter as tk
from tkinter import Canvas, Text, Button, PhotoImage, Label
from PIL import Image, ImageTk
import openai
import pyttsx3
import threading
import speech_recognition as sr
import os
import smtplib
import webbrowser
import wikipedia
import random
import requests
import shutil
import datetime
import logging
import psutil
from pathlib import Path

# Paths setup
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Files\Python Projects\Assistant\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Voice Assistant class
class VoiceAssistantApp:
    def __init__(self, window):
        self.window = window
        self.window.geometry("400x569")
        self.window.configure(bg="#FFFFFF")
        self.window.resizable(False, False)

        # Text-to-Speech engine initialization
        self.engine = pyttsx3.init()

        # Canvas setup
        self.canvas = tk.Canvas(
            window,
            bg="#FFFFFF",
            height=569,
            width=400,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Load images
        self.image_image_1 = tk.PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_image_2 = tk.PhotoImage(file=relative_to_assets("image_2.png"))
        self.image_image_3 = tk.PhotoImage(file=relative_to_assets("image_3.png"))
        self.button_image_1 = tk.PhotoImage(file=relative_to_assets("button_1.png"))
        self.entry_image_1 = tk.PhotoImage(file=relative_to_assets("entry_1.png"))

        # Create canvas elements
        self.canvas.create_image(200.0, 22.0, image=self.image_image_1)
        self.canvas.create_image(23.0, 22.0, image=self.image_image_2)
        self.canvas.create_text(36.0, 0.0, anchor="nw", text="Voice Assistant", fill="#FFFFFF", font=("MontserratRoman SemiBold", 32 * -1))
        self.canvas.create_image(200.0, 307.0, image=self.image_image_3)

        # Start button to trigger voice recognition
        self.button_1 = tk.Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.start_listening,
            relief="flat"
        )
        self.button_1.place(x=186.0, y=349.0, width=29.0, height=28.0)

        # Entry box for logs
        self.entry_bg_1 = self.canvas.create_image(199.0, 522.5, image=self.entry_image_1)
        self.entry_1 = tk.Text(
            bd=0,
            bg="#202020",
            fg="#FFFFFF",  # Changed the text color to white for better contrast
            highlightthickness=0
        )
        self.entry_1.place(x=0.0, y=476.0, width=398.0, height=91.0)
        self.entry_1.config(state='disabled')
        
        #Console Log Display (Label instead of Text)
        self.console_log = Label(self.window, bg="#000000", fg="white", wraplength=380, justify=tk.LEFT, anchor="nw", bd=0)
        self.console_log.place(x=0, y=480, width=0, height=0)  # Adjusted size and position
        
        
        
    OPENWEATHERMAP_API_KEY = "REPLACE_WITH_YOUR_OPENWEATHERMAP_API_KEY"
        
    def log_response(self, text):
        """Logs the conversation into the entry box."""
        self.entry_1.config(state='normal')
        self.entry_1.insert(tk.END, text + "\n")
        self.entry_1.config(state='disabled')
        self.entry_1.see(tk.END)

    def speak(self, text):
        """Speaks the given text."""
        self.engine.say(text)
        self.engine.runAndWait()

    def get_weather(self, city):
        api_key = self.OPENWEATHERMAP_API_KEY
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(base_url)
        data = response.json()
        if data["cod"] == 200:
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            return f"The temperature in {city} is {temperature}°C with {description}."
        else:
            return "Sorry, I couldn't fetch the weather information."

    def tell_joke(self):
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Parallel lines have so much in common. It’s a shame they’ll never meet.",
            "I only know 25 letters of the alphabet. I don't know y.",
            "I'm reading a book on anti-gravity. It's impossible to put down!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "What's the best thing about Switzerland? The flag is a big plus.",
            "I went to the aquarium this weekend, but I didn’t stay long. There’s something fishy about that place.",
            "I found a lion in my closet the other day! When I asked what it was doing there, it said Narnia business.",
            "What's a cat's favorite instrument? Purr-cussion.",
            "Why did the snail paint a giant S on his car? So when he drove by, people could say: Look at that S car go!",
            "What do you call a happy cowboy? A jolly rancher.",
            "What subject do cats like best in school? Hiss-tory.",
            "Humpty Dumpty had a great fall. He said his summer was pretty good too.",
            "My boss said dress for the job you want, not for the job you have. So I went in as Batman.",
            "How do you make holy water? You boil the hell out of it.",
            "Justice is a dish best served cold. Otherwise, it's just water.",
            "Why should you never throw grandpa's false teeth at a vehicle? You might denture car.",
            "Why are Christmas trees bad at knitting? They always drop their needles."
        ]
        return random.choice(jokes)
    
    def stop_voice_assistant(self):
        self.update_console_log("Assistant stopped.")
        self.speak("Stopping the assistant.")

    def leave_assistant(self):
        self.update_console_log("Assistant is leaving. Goodbye!")
        self.speak("Goodbye!")
        self.window.destroy()
    
    def get_date_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")
        return f"The current time is {current_time} and the date is {current_date}."

    def handle_email(self, recognizer):
        self.speak("Whom should I send the email to?")
        receiver_query = self.listen(recognizer)
        self.log_response(receiver_query)
        if receiver_query:
            self.speak("What should be the subject of the email?")
            subject_query = self.listen(recognizer)
            self.log_response(subject_query)
            if subject_query:
                self.speak("What message would you like to send?")
                message_query = self.listen(recognizer)
                self.log_response(message_query)
                if message_query:
                    email_result = self.send_email(receiver_query, subject_query, message_query)
                    self.speak(email_result)
                    self.log_response(email_result)
    def play_music_on_youtube(self, song_name):
        query = song_name.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        self.open_website(url)
    
    def create_folder(self, folder_name):
        try:
            os.makedirs(folder_name, exist_ok=True)
            return f"Folder '{folder_name}' created successfully."
        except Exception as e:
            return f"An error occurred while creating the folder: {str(e)}"

    def delete_folder(self, folder_name):
        try:
            shutil.rmtree(folder_name)
            return f"Folder '{folder_name}' deleted successfully."
        except Exception as e:
            return f"An error occurred while deleting the folder: {str(e)}"

    def rename_folder(self, old_name, new_name):
        try:
            os.rename(old_name, new_name)
            return f"Folder '{old_name}' renamed to '{new_name}' successfully."
        except Exception as e:
            return f"An error occurred while renaming the folder: {str(e)}"

    def move_to_directory(self, target_directory):
        try:
            os.chdir(target_directory)
            return f"Moved to directory '{target_directory}'."
        except Exception as e:
            return f"An error occurred while moving to the directory: {str(e)}"
    
    def open_telegram_app(self):
        try:
            os.startfile("C:\\Users\\User\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")
            return "Opening Telegram app."
        except Exception as e:
            return f"An error occurred while opening Telegram: {str(e)}"

    def search_wikipedia(self, query):
        try:
            result = wikipedia.summary(query, sentences=2)
            return result
        except wikipedia.exceptions.DisambiguationError as e:
            options = e.options[:5]
            return f"Multiple results found: {', '.join(options)}"

    def play_game(self):
        return "Sure! Let's play a game. I'm thinking of a number between 1 and 100. Try to guess it!"

    def open_program(self, program_name):
        try:
            os.startfile(program_name)
        except Exception as e:
            self.update_console_log(str(e))
            self.speak("Sorry, I couldn't open the program.")

    def open_website(self, website_url):
        try:
            webbrowser.open(website_url)
        except Exception as e:
            self.update_console_log(str(e))
            self.speak("Sorry, I couldn't open the website.")
    
    def handle_open_website(self, recognizer):
        self.speak("Sure, which website would you like to open?")
        website_query = self.listen(recognizer)
        self.log_response(website_query)
        if website_query:
            self.open_website("https://" + website_query)

    def handle_play_music(self, recognizer):
        self.speak("Sure, what song would you like to listen to?")
        song_query = self.listen(recognizer)
        self.log_response(song_query)
        if song_query:
            self.play_music_on_youtube(song_query)

    def handle_play_video(self, recognizer):
        self.speak("Sure, what video would you like to watch?")
        video_query = self.listen(recognizer)
        self.log_response(video_query)
        if video_query:
            self.play_music_on_youtube(video_query)
    
    def open_this_computer(self):
        try:
            os.startfile(".")
            return "Opening 'This PC' or 'My Computer'."
        except Exception as e:
            return f"An error occurred while opening 'This PC': {str(e)}"
        
    def open_program(self, program_name):
        try:
            os.startfile(program_name)
        except Exception as e:
            self.update_console_log(str(e))
            self.speak("Sorry, I couldn't open the program.")
            
    def close_application(self, app_name):
        for process in psutil.process_iter(['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                pid = process.info['pid']
                p = psutil.Process(pid)
                p.terminate()
                return f"Application '{app_name}' has been closed."
        return f"No running instance of '{app_name}' found."
    
    def handle_close_application(self, recognizer):
        self.speak("Sure, which program would you like to close?")
        close_query = self.listen(recognizer)
        self.log_response(close_query)
        if close_query:
            close_result = self.close_application(close_query)
            self.speak(close_result)
            self.log_response(close_result)
            
    def process_query(self, query):
        
        recognizer = sr.Recognizer()
        
        if "hello" in query.lower():
            self.speak("Good part of the day!")
        elif "what's up" in query.lower() or "how are you" in query.lower():
            self.speak("Great! What can I do for you?")
        elif "open main folder" in query.lower():
            result = self.open_this_computer()
            self.speak(result)
            self.log_response(result)
        elif "weather" in query.lower():
            city = query.split("weather in ")[-1]
            weather_info = self.get_weather(city)
            self.speak(weather_info)
            self.log_response(weather_info)
        elif "joke" in query.lower():
            joke = self.tell_joke()
            self.speak(joke)
            self.log_response(joke)
        elif "date" in query.lower() or "time" in query.lower():
            date_time = self.get_date_time()
            self.speak(date_time)
            self.log_response(date_time)
        elif "email" in query.lower():
            self.handle_email(recognizer)
        elif "create folder" in query.lower():
            folder_name = query.split("create folder ")[-1]
            result = self.create_folder(folder_name)
            self.speak(result)
            self.log_response(result)
        elif "delete folder" in query.lower():
            folder_name = query.split("delete folder ")[-1]
            result = self.delete_folder(folder_name)
            self.speak(result)
            self.log_response(result)
        elif "rename folder" in query.lower():
            query_parts = query.split("rename folder ")[-1].split(" to ")
            old_name, new_name = query_parts[0], query_parts[1]
            result = self.rename_folder(old_name, new_name)
            self.speak(result)
            self.log_response(result)
        elif "move to directory" in query.lower():
            target_directory = query.split("move to directory ")[-1]
            result = self.move_to_directory(target_directory)
            self.speak(result)
            self.log_response(result)
        elif "open telegram" in query.lower():
            result = self.open_telegram_app()
            self.speak(result)
            self.log_response(result)
        elif "search" in query.lower():
            search_query = query.split("search for ")[-1]
            search_result = self.search_wikipedia(search_query)
            self.speak(search_result)
            self.log_response(search_result)
        elif "play game" in query.lower():
            game_info = self.play_game()
            self.speak(game_info)
            self.log_response(game_info)
        elif "telegram" in query.lower() or "messenger" in query.lower():
            self.open_program("Telegram.exe")
        elif "chrome" in query.lower():
            self.open_program("chrome.exe")
        elif "youtube" in query.lower():
            self.open_website("https://www.youtube.com")
        elif "desmos" in query.lower():
            self.open_website("https://www.desmos.com/calculator?lang=ru")
        elif "spotify" in query.lower():
            self.open_program("spotify.exe")
        elif "steam" in query.lower():
            self.open_program("steam.exe")
        elif "calculator" in query.lower():
            self.open_program("calc.exe")
        elif "this computer" in query.lower():
            self.open_program("explorer.exe")
        elif "open website" in query.lower():
            self.handle_open_website(recognizer)
        elif "play music" in query.lower():
            self.handle_play_music(recognizer)
        elif "open video" in query.lower():
            self.handle_play_video(recognizer)
        elif "open all play" in query.lower() or "open allplay" in query.lower():
            self.open_website("https://allplay.uz/")
        elif "close program" in query.lower() or "close application" in query.lower():
            self.handle_close_application(recognizer)
        elif "stop assistant" in query.lower():
            self.stop_voice_assistant()
            return  # End loop and thread
        elif "leave assistant" in query.lower():
            self.leave_assistant()
            return  # End loop and thread
        else:
            self.speak("Unknown command")
            self.log_response("Unknown command: " + query)

    def ask_gpt(self, query):
        """Sends the query to GPT-3.5 and returns the response."""
        openai.api_key = 'REPLACE_WITH_YOUR_OPENAI_API_KEY'
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=query,
            max_tokens=50
        )
        return response.choices[0].text.strip()

    def listen_and_process(self):
        self.log_response("Hello! How can I assist you?")
        
        recognizer = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                self.log_response("Listening...")
                audio = recognizer.listen(source)

                try:
                    query = recognizer.recognize_google(audio)
                    self.log_response(f"You: {query}")
                    self.process_query(query)
                except sr.UnknownValueError:
                    response = "Sorry, I could not understand the audio."
                    self.speak(response)
                    self.log_response(f"Assistant: {response}")
                except sr.RequestError:
                    response = "Sorry, my speech service is down."
                    self.speak(response)
                    self.log_response(f"Assistant: {response}")
                
    def update_console_log(self, message):
        self.console_log.config(state=tk.NORMAL)
        self.console_log.insert(tk.END, message + '\n')
        self.console_log.see(tk.END)
        self.console_log.config(state=tk.DISABLED)

    def start_listening(self):
        """Starts the listening process in a separate thread."""
        threading.Thread(target=self.listen_and_process).start()
        
# Main function to run the app
def main():
    window = tk.Tk()
    app = VoiceAssistantApp(window)
    window.mainloop()

if __name__ == "__main__":
    main()