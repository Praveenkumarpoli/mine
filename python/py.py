import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import requests

# Initialize the recognizer and pyttsx3 engine
recognizer = sr.Recognizer()

# Initialize the pyttsx3 engine
engine = pyttsx3.init()

def speak(text):
    """Function to convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Function to listen to user's voice command"""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")
        return None
    except sr.RequestError:
        print("Sorry, I'm having trouble with the speech service.")
        return None

def wish_user():
    """Function to greet the user based on the time of day"""
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")

def get_weather(city):
    """Fetch weather information from OpenWeatherMap API"""
    api_key = "your_openweathermap_api_key"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] == 200:
            main = data["main"]
            weather = data["weather"][0]
            temp = main["temp"]
            description = weather["description"]
            speak(f"The temperature in {city} is {temp} degrees Celsius with {description}.")
        else:
            speak("Sorry, I couldn't find the weather for that location.")
    except Exception as e:
        print(e)
        speak("Sorry, I couldn't fetch the weather information right now.")

def open_website(query):
    """Search and open a website"""
    query = query.replace("open", "").strip()
    webbrowser.open(f"https://www.{query}.com")
    speak(f"Opening {query} website.")

def search_google(query):
    """Search Google with a query"""
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching Google for {query}.")

def open_application(app_name):
    """Open an application installed on the computer"""
    app_name = app_name.lower()
    if "chrome" in app_name:
        os.system("start chrome")  # Works on Windows
        speak("Opening Google Chrome.")
    elif "notepad" in app_name:
        os.system("notepad")  # Works on Windows
        speak("Opening Notepad.")
    elif "calculator" in app_name:
        os.system("calc")  # Works on Windows
        speak("Opening Calculator.")
    else:
        speak("Sorry, I can't open that application.")

def main():
    """Main function to run the assistant"""
    wish_user()
    speak("How can I assist you?")
    
    while True:
        command = listen()

        if command:
            if 'hello' in command:
                speak("Hello! How can I help you today?")
            elif 'time' in command:
                now = datetime.datetime.now().strftime("%H:%M")
                speak(f"The current time is {now}")
            elif 'weather' in command:
                city = command.replace("weather in", "").strip()
                if city:
                    get_weather(city)
                else:
                    speak("Please mention the city for weather information.")
            elif 'open' in command:
                open_website(command)
            elif 'search' in command:
                search_google(command.replace("search", "").strip())
            elif 'open' in command:
                open_application(command)
            elif 'stop' in command or 'exit' in command:
                speak("Goodbye! Have a great day!")
                break
            else:
                speak("Sorry, I didn't catch that.")

if __name__ == "__main__":
    main()
