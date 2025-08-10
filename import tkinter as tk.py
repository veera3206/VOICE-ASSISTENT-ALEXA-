import tkinter as tk
from tkinter import Label, Frame, Button, scrolledtext
import speech_recognition as sr
import pyttsx3
import threading
from datetime import datetime, timedelta
import webbrowser
import pywhatkit as kit
import wikipedia
import os

# Define the assistant's name
assistant_name = "Alexa"

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# List available voices and set a voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"Speaking: {text}")  # Debugging statement
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        label.config(text="Listening...", fg="#00FF00")  # Green text for listening state
        root.update()
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            label.config(text=f"You said: {command}", fg="#FFFFFF")  # White text for user input
            root.update()
            process_command(command.lower())
        except sr.UnknownValueError:
            label.config(text="Sorry, I didn't understand.", fg="#FF0000")  # Red text for errors
        except sr.RequestError:
            label.config(text="API unavailable.", fg="#FF0000")
        except sr.WaitTimeoutError:
            label.config(text="No speech detected.", fg="#FF0000")
        root.update()

def process_command(command):
    response = ""

    if "hello" in command:
        response = "Hello! How can I help you?"
    elif "your name" in command:
        response = "I am your voice assistant."
    elif "thank you" in command:
        response = "You're welcome! If you need anything else, just let me know."
    elif "time" in command:
        now = datetime.now()
        response = now.strftime("The time is %H:%M:%S")
    elif "today" in command and "date" in command:
        now = datetime.now()
        response = now.strftime("Today's date is %B %d, %Y")
    elif "tomorrow" in command and "date" in command:
        tomorrow = datetime.now() + timedelta(days=1)
        response = tomorrow.strftime("Tomorrow's date is %B %d, %Y")
    elif "yesterday" in command and "date" in command:
        yesterday = datetime.now() - timedelta(days=1)
        response = yesterday.strftime("Yesterday's date was %B %d, %Y")
    elif "add" in command:
        numbers = [int(s) for s in command.split() if s.isdigit()]
        if len(numbers) >= 2:
            response = f"The sum of {numbers} is {sum(numbers)}"
        else:
            response = "Please specify at least two numbers."
    elif "subtraction" in command or "subtract" in command:
        numbers = [int(s) for s in command.split() if s.isdigit()]
        if len(numbers) == 2:
            response = f"The difference of {numbers} is {numbers[0] - numbers[1]}"
        else:
            response = "Please specify exactly two numbers."
    elif "multiply" in command:
        numbers = [int(s) for s in command.split() if s.isdigit()]
        if len(numbers) == 2:
            response = f"The product of {numbers} is {numbers[0] * numbers[1]}"
        else:
            response = "Please specify exactly two numbers."
    elif "divide" in command:
        numbers = [int(s) for s in command.split() if s.isdigit()]
        if len(numbers) == 2 and numbers[1] != 0:
            response = f"The quotient of {numbers} is {numbers[0] / numbers[1]:.2f}"
        else:
            response = "Please specify two numbers, and make sure the divisor is not zero."
    elif "search" in command:
        search_term = command.replace("search", "").strip()
        response = f"Searching for {search_term}"
        webbrowser.open(f"https://www.google.com/search?q={search_term}")
    elif "play" in command:
        song = command.replace("play", "").strip()
        response = f"Playing {song} on YouTube"
        kit.playonyt(song)
    elif "who is" in command or "what is" in command or "tell me about" in command:
        search_term = command.replace("who is", "").replace("what is", "").replace("tell me about", "").strip()
        try:
            response = wikipedia.summary(search_term, sentences=2)
        except wikipedia.exceptions.DisambiguationError:
            response = f"Multiple results found for {search_term}. Please be more specific."
        except wikipedia.exceptions.PageError:
            webbrowser.open(f"https://www.google.com/search?q={search_term}")
            response = f"I have opened a Google search for {search_term}."
    elif "open" in command:
        app = command.replace("open", "").strip()
        if "chrome" in app:
            response = "Opening Google Chrome"
            os.system("start chrome")
        elif "notepad" in app:
            response = "Opening Notepad"
            os.system("start notepad")
        else:
            response = f"Opening {app} in browser"
            webbrowser.open(f"https://www.{app}.com")
    elif "news" in command:
        response = "Opening latest news."
        webbrowser.open("https://news.google.com/")
    elif "exit" in command:
        response = "Goodbye!"
        speak(response)
        root.destroy()

    speak(response)
    response_text.insert(tk.END, f"\n{response}\n")
    response_text.yview(tk.END)

def start_listening():
    threading.Thread(target=recognize_speech, daemon=True).start()

def create_ui(root):
    main_frame = Frame(root, bg="#1E1E1E")
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    Label(main_frame, text="Voice Assistant", font=("Helvetica", 24, "bold"), fg="#00FF00", bg="#1E1E1E").pack(pady=10)

    global response_text, label
    response_text = scrolledtext.ScrolledText(main_frame, font=("Arial", 12), fg="#FFFFFF", bg="#282828", wrap=tk.WORD, height=8)
    response_text.pack(pady=10, fill=tk.X)

    label = Label(main_frame, text="Click the button & speak", font=("Arial", 14), fg="#FFFFFF", bg="#1E1E1E")
    label.pack(pady=10)

    Button(main_frame, text="Speak", command=start_listening, font=("Arial", 14), bg="#00A86B", fg="#FFFFFF", padx=20, pady=10, bd=0).pack(pady=10)
    Button(main_frame, text="Close", command=root.destroy, font=("Arial", 12), bg="#FF0000", fg="#FFFFFF", padx=10, pady=5, bd=0).pack(pady=10)

root = tk.Tk()
root.title("Voice Assistant")
root.geometry("600x500")
root.configure(bg="#1E1E1E")

create_ui(root)
root.bind("<Escape>", lambda event: root.destroy())
root.mainloop()