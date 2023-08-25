import tkinter as tk
import pyttsx3
import speech_recognition as sr
import webbrowser
import os
import threading
import logging
from PIL import Image, ImageTk
import requests
import random
import datetime
import smtplib
import wikipedia
import shutil


def setup_logging():
    logging.basicConfig(filename='voice_assistant.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def open_this_computer():
    try:
        os.startfile(".")
        return "Opening 'This PC' or 'My Computer'."
    except Exception as e:
        return f"An error occurred while opening 'This PC': {str(e)}"


def log_response(response):
    logging.info(response)
    console_log.config(state=tk.NORMAL)  # Enable writing to the console log
    console_log.insert(tk.END, "Assistant: " + response + '\n')
    console_log.config(state=tk.DISABLED)  # Disable writing to the console log


def create_folder(folder_name):
    try:
        os.makedirs(folder_name, exist_ok=True)
        return f"Folder '{folder_name}' created successfully."
    except Exception as e:
        return f"An error occurred while creating the folder: {str(e)}"


def delete_folder(folder_name):
    try:
        shutil.rmtree(folder_name)
        return f"Folder '{folder_name}' deleted successfully."
    except Exception as e:
        return f"An error occurred while deleting the folder: {str(e)}"


def rename_folder(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        return f"Folder '{old_name}' renamed to '{new_name}' successfully."
    except Exception as e:
        return f"An error occurred while renaming the folder: {str(e)}"


def move_to_directory(target_directory):
    try:
        os.chdir(target_directory)
        return f"Moved to directory '{target_directory}'."
    except Exception as e:
        return f"An error occurred while moving to the directory: {str(e)}"


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def get_weather(city):
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


def open_telegram_app():
    try:
        os.startfile("C:\\Users\\User\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe")   # Путь к исполняемому файлу Telegram
        return "Opening Telegram app."
    except Exception as e:
        return f"An error occurred while opening Telegram: {str(e)}"


def tell_joke():
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Parallel lines have so much in common. It’s a shame they’ll never meet.",
        "I only know 25 letters of the alphabet. I don't know y.",
        "I'm reading a book on anti-gravity. It's impossible to put down!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
    ]
    return random.choice(jokes)


def get_date_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    current_date = now.strftime("%Y-%m-%d")
    return f"The current time is {current_time} and the date is {current_date}."


def open_photoshop_app():
    try:
        os.startfile(
            "C:\Program Files\Adobe\Adobe Photoshop (Beta)\Photoshop.exe")  # Путь к исполняемому файлу Adobe Photoshop
        return "Opening Adobe Photoshop app."
    except Exception as e:
        return f"An error occurred while opening Adobe Photoshop: {str(e)}"


def open_premiere_pro_app():
    try:
        os.startfile(
            "C:\Program Files\Adobe\Adobe Premiere Pro 2023\Adobe Premiere Pro.exe")  # Путь к исполняемому файлу Adobe Premiere Pro
        return "Opening Adobe Premiere Pro app."
    except Exception as e:
        return f"An error occurred while opening Adobe Premiere Pro: {str(e)}"


def open_audition_app():
    try:
        os.startfile(
            "C:\Program Files\Adobe\Adobe Audition 2023\Adobe Audition.exe")  # Путь к исполняемому файлу Adobe Audition
        return "Opening Adobe Audition app."
    except Exception as e:
        return f"An error occurred while opening Adobe Audition: {str(e)}"


def send_email(receiver_email, subject, message):
    sender_email = "flash369636@gmail.com"
    sender_password = "Sherbek369636"
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        email_text = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, receiver_email, email_text)
        server.quit()
        return "Email sent successfully."
    except Exception as e:
        return f"Error sending email: {str(e)}"


def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:5]
        return f"Multiple results found: {', '.join(options)}"


def play_game():
    return "Sure! Let's play a game. I'm thinking of a number between 1 and 100. Try to guess it!"


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        console_log.config(state=tk.NORMAL)  # Enable writing to the console log
        console_log.insert(tk.END, "Listening...\n")
        console_log.config(state=tk.DISABLED)  # Disable writing to the console log
        try:
            audio = recognizer.listen(source, timeout=3)  # Set listening time to 3 seconds
            console_log.config(state=tk.NORMAL)  # Enable writing to the console log
            console_log.insert(tk.END, "Recognizing...\n")
            console_log.config(state=tk.DISABLED)  # Disable writing to the console log
            query = recognizer.recognize_google(audio)
            console_log.config(state=tk.NORMAL)  # Enable writing to the console log
            console_log.insert(tk.END, "You said: " + query + '\n')
            console_log.config(state=tk.DISABLED)  # Disable writing to the console log
            return query.lower()
        except sr.WaitTimeoutError:
            console_log.config(state=tk.NORMAL)  # Enable writing to the console log
            console_log.insert(tk.END, "Listening timed out. Please try again.\n")
            console_log.config(state=tk.DISABLED)  # Disable writing to the console log
            return ""
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

        if "open main folder" in query:
            result = open_this_computer()
            speak(result)
            log_response(result)
        elif "weather" in query:
            city = query.split("weather in ")[-1]
            weather_info = get_weather(city)
            speak(weather_info)
            log_response(weather_info)
        elif "joke" in query:
            joke = tell_joke()
            speak(joke)
            log_response(joke)
        elif "date" in query or "time" in query:
            date_time = get_date_time()
            speak(date_time)
            log_response(date_time)
        elif "email" in query:
            speak("Whom should I send the email to?")
            receiver_query = listen()
            log_response(receiver_query)
            if receiver_query:
                speak("What should be the subject of the email?")
                subject_query = listen()
                log_response(subject_query)
                if subject_query:
                    speak("What message would you like to send?")
                    message_query = listen()
                    log_response(message_query)
                    if message_query:
                        email_result = send_email(receiver_query, subject_query, message_query)
                        speak(email_result)
                        log_response(email_result)
        elif "create folder" in query:
            folder_name = query.split("create folder ")[-1]
            result = create_folder(folder_name)
            speak(result)
            log_response(result)
        elif "open telegram" in query:
            result = open_telegram_app()
            speak(result)
            log_response(result)
        elif "delete folder" in query:
            folder_name = query.split("delete folder ")[-1]
            result = delete_folder(folder_name)
            speak(result)
            log_response(result)
        elif "rename folder" in query:
            query_parts = query.split("rename folder ")[-1].split(" to ")
            old_name, new_name = query_parts[0], query_parts[1]
            result = rename_folder(old_name, new_name)
            speak(result)
            log_response(result)
        elif "move to directory" in query:
            target_directory = query.split("move to directory ")[-1]
            result = move_to_directory(target_directory)
            speak(result)
            log_response(result)
        elif "search" in query:
            search_query = query.split("search for ")[-1]
            search_result = search_wikipedia(search_query)
            speak(search_result)
            log_response(search_result)
        elif "play game" in query:
            game_info = play_game()
            speak(game_info)
            log_response(game_info)
        elif "telegram" in query or "messenger" in query:
            open_program("Telegram.exe")
        elif "chrome" in query:
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
            speak("Sure, what video would you like to watch?")
            video_query = listen()
            log_response(video_query)
            if video_query:
                play_music_on_youtube(video_query)
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
    root.resizable(False, False)  # Prevent window resizing

    setup_logging()

    # Load the background image
    background_image = Image.open("bgfile\wallground.jpg")
    background_photo = ImageTk.PhotoImage(background_image)

    # Create a label to display the background image
    background_label = tk.Label(root, image=background_photo)
    background_label.pack(fill=tk.BOTH, expand=True)  # Fit to the size of the photo

    # Create the "Start Assistant" button
    def start_voice_assistant_thread():
        threading.Thread(target=start_voice_assistant).start()

    button = tk.Button(root, text="Start Assistant", command=start_voice_assistant_thread)
    button.pack(pady=10)

    # Create a console log inside the application
    global console_log
    console_log = tk.Text(root, bg="#000000", fg="white", wrap=tk.WORD, state=tk.NORMAL, height=10, bd=0,
                          highlightthickness=0)
    console_log.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
