from pathlib import Path
from tkinter import Tk, Canvas, Text, Button, PhotoImage
from PIL import Image, ImageTk
import threading
import tkinter as tk
import pyttsx3
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

from Assistant.gui import relative_to_assets, canvas


class VoiceAssistantApp:
    API_KEY = "YOUR_TOKEN_HERE"
    SENDER_EMAIL = "YOUR_EMAIL_HERE"
    SENDER_PASSWORD = "YOUR_PASSWORD_HERE"

    def __init__(self, root):
        self.root = root
        self.root.title("Voice Assistant")
        self.root.resizable(False, False)

        self.setup_logging()

        self.background_photo = ImageTk.PhotoImage(Image.open("bgfile\wallground.jpg"))

        self.create_gui()
        self.engine = self.initialize_speech_engine()

    def setup_logging(self):
        logging.basicConfig(filename='voice_assistant.log', level=logging.INFO, format='%(asctime)s - %(message)s')

    def initialize_speech_engine(self):
        return pyttsx3.init()

    def create_gui(self):
        background_label = tk.Label(self.root, image=self.background_photo)
        background_label.pack(fill=tk.BOTH, expand=True)

        start_button = Button(self.root, text="Start Assistant", command=self.start_voice_assistant_thread)
        start_button.pack(pady=10)

        self.console_log = Text(self.root, bg="#000000", fg="white", wrap=tk.WORD, state=tk.NORMAL, height=10, bd=0,
                                highlightthickness=0)
        self.console_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def start_voice_assistant_thread(self):
        threading.Thread(target=self.start_voice_assistant).start()

    def close_application(self, app_name):
        for process in psutil.process_iter(['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                pid = process.info['pid']
                p = psutil.Process(pid)
                p.terminate()
                return f"Application '{app_name}' has been closed."
        return f"No running instance of '{app_name}' found."

    def calculator_operation(operation, num1, num2):
        if operation == 'add':
            result = num1 + num2
        elif operation == 'subtract':
            result = num1 - num2
        elif operation == 'multiply':
            result = num1 * num2
        elif operation == 'divide':
            if num2 != 0:
                result = num1 / num2
            else:
                return "Error: Division by zero"
        else:
            return "Error: Invalid operation"

        return result

    def start_voice_assistant(self):
        self.log_response("Hello! How can I assist you?")

        recognizer = sr.Recognizer()

        while True:
            query = self.listen(recognizer)
            self.log_response(query)

            if "hello" in query.lower():
                self.speak("Good part of the day!")
            elif "what's up" in query.lower() or "how are you" in query.lower():
                self.speak("Great! What can I do for you?")

            if "open main folder" in query:
                result = self.open_this_computer()
                self.speak(result)
                self.log_response(result)
            elif "weather" in query:
                city = query.split("weather in ")[-1]
                weather_info = self.get_weather(city)
                self.speak(weather_info)
                self.log_response(weather_info)
            elif "joke" in query:
                joke = self.tell_joke()
                self.speak(joke)
                self.log_response(joke)
            elif "date" in query or "time" in query:
                date_time = self.get_date_time()
                self.speak(date_time)
                self.log_response(date_time)
            elif "email" in query:
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
            elif "create folder" in query:
                folder_name = query.split("create folder ")[-1]
                result = self.create_folder(folder_name)
                self.speak(result)
                self.log_response(result)
            elif "open telegram" in query:
                result = self.open_telegram_app()
                self.speak(result)
                self.log_response(result)
            elif "delete folder" in query:
                folder_name = query.split("delete folder ")[-1]
                result = self.delete_folder(folder_name)
                self.speak(result)
                self.log_response(result)
            elif "rename folder" in query:
                query_parts = query.split("rename folder ")[-1].split(" to ")
                old_name, new_name = query_parts[0], query_parts[1]
                result = self.rename_folder(old_name, new_name)
                self.speak(result)
                self.log_response(result)
            elif "move to directory" in query:
                target_directory = query.split("move to directory ")[-1]
                result = self.move_to_directory(target_directory)
                self.speak(result)
                self.log_response(result)
            elif "search" in query:
                search_query = query.split("search for ")[-1]
                search_result = self.search_wikipedia(search_query)
                self.speak(search_result)
                self.log_response(search_result)
            elif "play game" in query:
                game_info = self.play_game()
                self.speak(game_info)
                self.log_response(game_info)
            elif "telegram" in query or "messenger" in query:
                self.open_program("Telegram.exe")
            elif "chrome" in query:
                self.open_program("chrome.exe")
            elif "youtube" in query:
                self.open_website("https://www.youtube.com")
            elif "desmos" in query:
                self.open_website("https://www.desmos.com/calculator?lang=ru")
            elif "spotify" in query:
                self.open_program("spotify.exe")
            elif "steam" in query:
                self.open_program("steam.exe")
            elif "calculator" in query:
                self.open_program("calc.exe")
            elif "this computer" in query:
                self.open_program("explorer.exe")
            elif "open website" in query:
                self.speak("Sure, which website would you like to open?")
                website_query = self.listen(recognizer)
                self.log_response(website_query)
                if website_query:
                    self.open_website("https://" + website_query)
            elif "play music" in query:
                self.speak("Sure, what song would you like to listen to?")
                song_query = self.listen(recognizer)
                self.log_response(song_query)
                if song_query:
                    self.play_music_on_youtube(song_query)
            elif "open video" in query:
                self.speak("Sure, what video would you like to watch?")
                video_query = self.listen(recognizer)
                self.log_response(video_query)
                if video_query:
                    self.play_music_on_youtube(video_query)
            elif "open all play" in query or "open allplay" in query:
                self.open_website("https://allplay.uz/")
            elif "close program" in query or "close application" in query:  # Modify this line
                self.speak("Sure, which program would you like to close?")
                close_query = self.listen(recognizer)
                self.log_response(close_query)
                if close_query:
                    close_result = self.close_application(close_query)  # Modify this line
                    self.speak(close_result)
                    self.log_response(close_result)
            elif "stop assistant" in query:
                self.stop_voice_assistant()
                break
            elif "leave assistant" in query:
                self.leave_assistant()
                break
            else:
                self.speak("Unknown command")
                self.log_response("Unknown command: " + query)


    def listen(self, recognizer):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            recognizer.energy_threshold = 4000

            self.update_console_log("Listening...")

            try:
                audio = recognizer.listen(source, timeout=5,
                                          phrase_time_limit=5)  # Adjust the timeout and phrase_time_limit as needed
                self.update_console_log("Recognizing...")
                query = recognizer.recognize_google(audio)
                self.update_console_log(f"You said: {query}")
                return query.lower()
            except sr.WaitTimeoutError:
                self.update_console_log("Listening timed out. Please try again.")
                return ""
            except sr.UnknownValueError:
                self.update_console_log("Sorry, I couldn't understand what you said.")
                return ""
            except sr.RequestError:
                self.update_console_log("Sorry, there was an issue with the speech recognition service.")
                return ""

    def open_this_computer(self):
        try:
            os.startfile(".")
            return "Opening 'This PC' or 'My Computer'."
        except Exception as e:
            return f"An error occurred while opening 'This PC': {str(e)}"

    def log_response(self, response):
        logging.info(response)
        self.update_console_log("Assistant: " + response)

    def update_console_log(self, message):
        self.console_log.config(state=tk.NORMAL)
        self.console_log.insert(tk.END, message + '\n')
        self.console_log.see(tk.END)  # Scroll to the end
        self.console_log.config(state=tk.DISABLED)

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def get_weather(self, city):
        api_key = "a85ae82c61fc4cb8c4b03016986dce09"
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
        ]
        return random.choice(jokes)

    def get_date_time(self):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%Y-%m-%d")
        return f"The current time is {current_time} and the date is {current_date}."

    def send_email(self, receiver_email, subject, message):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)
            email_text = f"Subject: {subject}\n\n{message}"
            server.sendmail(self.SENDER_EMAIL, receiver_email, email_text)
            server.quit()
            return "Email sent successfully."
        except smtplib.SMTPException as e:
            return f"Error sending email: {str(e)}"

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

    def play_music_on_youtube(self, song_name):
        query = song_name.replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        self.open_website(url)

    def stop_voice_assistant(self):
        self.update_console_log("Assistant stopped.")

    def leave_assistant(self):
        self.update_console_log("Assistant is leaving. Goodbye!")
        self.root.destroy()

class GUIApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x569")
        self.root.configure(bg="#FFFFFF")

        self.create_widgets()
        self.voice_assistant_app = VoiceAssistantApp(self.root)

    def create_widgets(self):
        # Your existing GUI code here...

        button_image_1 = PhotoImage(file="path_to_button_1.png")
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.voice_assistant_app.start_voice_assistant_thread,
            relief="flat"
        )
        button_1.place(x=186.0, y=349.0, width=29.0, height=28.0)

        image_image_3 = PhotoImage(
            file=relative_to_assets("image_3.png"))
        image_3 = canvas.create_image(
            200.0,
            307.0,
            image=image_image_3
        )

        entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            199.0,
            522.5,
            image=entry_image_1
        )
        entry_1 = Text(
            bd=0,
            bg="#202020",
            fg="#000716",
            highlightthickness=0,
            state=tk.DISABLED  # Set the state to DISABLED to make it non-editable
        )
        entry_1.place(
            x=0.0,
            y=476.0,
            width=398.0,
            height=91.0
        )


if __name__ == "__main__":
    window = Tk()
    app = GUIApp(window)
    window.mainloop()
