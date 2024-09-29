import speech_recognition as sr
import webbrowser
import pyttsx3  # Use for text-to-speech
import musicLibrary
import requests
from openai import OpenAI
import pygame
import os
from gtts import gTTS
# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

news_api = "cda991f84b424362a72bf3796f4f4417"  # You should store your API key securely

def speak_old(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save("temp.mp3")

        # Initialize the mixer module
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running to allow the music to play
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def process_command(command):
    """Process recognized voice command."""
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find the song {song}.")
    elif "news" in command:
        fetch_news()
    else:
        output = aiProcess(command)
        speak(output)
        pass

def aiProcess(command):
    client = OpenAI(
    api_key="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",
    )
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistent named jarvis skilled in general tasks like alexa."},
        {"role": "user", "content": command }
    ]
)

    return completion.choices[0].message.content


def fetch_news():
    """Fetch and read the latest headlines."""
    try:
        response = requests.get(f"https://newsapi.org/v2/top-headlines?sources=bbc-news&apiKey={news_api}")
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            if articles:
                speak("Here are the latest headlines:")
                for article in articles[:5]:  # Limit to top 5 articles
                    speak(article.get('title', 'No title available'))
            else:
                speak("I couldn't find any news articles.")
        else:
            speak("Failed to retrieve news.")
    except requests.RequestException as e:
        speak(f"Error retrieving news: {e}")
 
if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
            # Obtain audio from the microphone
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=1)

            # Recognize speech using Google Cloud API
            print("Recognizing...")
            word = recognizer.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Yes?")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis active. Listening for your command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)

                # Recognize command
                command = recognizer.recognize_google(audio)
                process_command(command)

                # Speak the recognized command
                speak(f"You said: {command}")

        except sr.UnknownValueError:
            print("Could not understand audio.")
        except sr.RequestError as e:
            print(f"Error with the Google Speech Recognition service: {e}")
        except Exception as e:
            print(f"Error: {e}")
