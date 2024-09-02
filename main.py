import customtkinter as ctk
import threading
import speech_recognition as sr
import pyttsx3
import openai
import requests
import wikipedia
import random
import os
import webbrowser
import psutil
from PIL import Image
import datetime
import config

class ARIA:
    def __init__(self, master):
        self.master = master
        self.master.title("ARIA - Artificially Responsive Intelligent Assistant")
        self.master.geometry("500x700")

        # Set the color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize TTS engine
        self.engine = pyttsx3.init()

        # Main frame
        self.main_frame = ctk.CTkFrame(self.master)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Logo
        logo_path = os.path.join("assets", "frame0", "aria_logo.png")
        self.logo = ctk.CTkImage(light_image=Image.open(logo_path),
                                 dark_image=Image.open(logo_path),
                                 size=(100, 100))
        self.logo_label = ctk.CTkLabel(self.main_frame, image=self.logo, text="")
        self.logo_label.pack(pady=20)

        # Title
        self.title_label = ctk.CTkLabel(self.main_frame, text="ARIA", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=10)

        # Chat display
        self.chat_display = ctk.CTkTextbox(self.main_frame, height=300, width=400, state="disabled")
        self.chat_display.pack(pady=20)

        # Input field
        self.input_field = ctk.CTkEntry(self.main_frame, placeholder_text="Type your message...", width=300)
        self.input_field.pack(side="left", padx=(20, 10))
        self.input_field.bind("<Return>", lambda event: self.send_message())

        # Send button
        self.send_button = ctk.CTkButton(self.main_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="left")

        # Microphone button
        self.mic_button = ctk.CTkButton(self.main_frame, text="🎤", width=40, command=self.start_listening)
        self.mic_button.pack(side="left", padx=10)

        # Status label
        self.status_label = ctk.CTkLabel(self.main_frame, text="")
        self.status_label.pack(pady=10)

        # Initialize API keys
        openai.api_key = config.OPENAI_API_KEY
        self.weather_api_key = config.OPENWEATHERMAP_API_KEY

    def send_message(self):
        message = self.input_field.get()
        if message:
            self.update_chat_display(f"You: {message}")
            self.input_field.delete(0, "end")
            threading.Thread(target=self.process_query, args=(message,)).start()

    def start_listening(self):
        self.status_label.configure(text="Listening...")
        threading.Thread(target=self.listen_and_process).start()

    def listen_and_process(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            self.update_chat_display(f"You: {query}")
            self.process_query(query)
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand the audio.")
        except sr.RequestError:
            self.speak("Sorry, my speech service is down.")
        finally:
            self.status_label.configure(text="")

    def process_query(self, query):
        query = query.lower()
        if "hello" in query:
            response = "Hello! How can I assist you today?"
        elif "weather" in query:
            city = query.split("weather in ")[-1]
            response = self.get_weather(city)
        elif "joke" in query:
            response = self.tell_joke()
        elif "time" in query:
            response = self.get_date_time()
        elif "search" in query:
            search_query = query.split("search for ")[-1]
            response = self.search_wikipedia(search_query)
        elif "open website" in query:
            website = query.split("open website ")[-1]
            self.open_website(f"https://{website}")
            response = f"Opening {website}"
        elif "open" in query:
            app = query.split("open ")[-1]
            self.open_program(f"{app}.exe")
            response = f"Opening {app}"
        elif "close" in query:
            app = query.split("close ")[-1]
            response = self.close_application(app)
        else:
            response = self.ask_gpt(query)
        
        self.update_chat_display(f"ARIA: {response}")
        self.speak(response)

    def update_chat_display(self, message):
        self.chat_display.configure(state="normal")
        self.chat_display.insert("end", message + "\n")
        self.chat_display.see("end")
        self.chat_display.configure(state="disabled")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def get_weather(self, city):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
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
            "Parallel lines have so much in common. It's a shame they'll never meet.",
            "I only know 25 letters of the alphabet. I don't know y.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]
        return random.choice(jokes)

    def get_date_time(self):
        now = datetime.datetime.now()
        return f"The current time is {now.strftime('%H:%M')} and the date is {now.strftime('%Y-%m-%d')}."

    def search_wikipedia(self, query):
        try:
            return wikipedia.summary(query, sentences=2)
        except wikipedia.exceptions.DisambiguationError as e:
            return f"Multiple results found: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            return f"Sorry, I couldn't find any information about {query}."

    def open_website(self, url):
        webbrowser.open(url)

    def open_program(self, program_name):
        try:
            os.startfile(program_name)
        except FileNotFoundError:
            self.speak(f"Sorry, I couldn't find the program {program_name}.")

    def close_application(self, app_name):
        for process in psutil.process_iter(['pid', 'name']):
            if app_name.lower() in process.info['name'].lower():
                psutil.Process(process.info['pid']).terminate()
                return f"Closed {app_name}."
        return f"Couldn't find {app_name} running."

    def ask_gpt(self, query):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=query,
            max_tokens=150
        )
        return response.choices[0].text.strip()

if __name__ == "__main__":
    root = ctk.CTk()
    app = ARIA(root)
    root.mainloop()