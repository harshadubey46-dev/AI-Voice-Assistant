import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia


# --------------------------------------------------
# Initialize Voice Assistant
# --------------------------------------------------

recognizer = sr.Recognizer()
engine = pyttsx3.init()


# --------------------------------------------------
# Text-to-Speech
# --------------------------------------------------

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()


# --------------------------------------------------
# Get Voice Input
# --------------------------------------------------

def listen():
    with sr.Microphone() as source:

        print("\nListening... 🎙️")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            print("Recognizing...")

            query = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You:", query)

            return query.lower()

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

        except sr.UnknownValueError:
            speak("Sorry, I could not understand what you said.")
            return ""

        except sr.RequestError:
            speak("Sorry, the speech recognition service is unavailable.")
            return ""


# --------------------------------------------------
# Process Commands
# --------------------------------------------------

def process_command(query):

    if "hello" in query or "hi" in query:
        speak("Hello! How can I help you?")

    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today's date is {current_date}.")

    elif "open google" in query:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "open youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "open github" in query:
        speak("Opening GitHub.")
        webbrowser.open("https://github.com")

    elif "wikipedia" in query or "who is" in query or "what is" in query:

        search_query = query

        if "wikipedia" in search_query:
            search_query = search_query.replace("wikipedia", "").strip()

        elif "who is" in search_query:
            search_query = search_query.replace("who is", "").strip()

        elif "what is" in search_query:
            search_query = search_query.replace("what is", "").strip()

        if search_query:

            try:
                speak(f"Searching Wikipedia for {search_query}.")

                result = wikipedia.summary(
                    search_query,
                    sentences=2
                )

                speak(result)

            except wikipedia.exceptions.DisambiguationError:
                speak("There are multiple results for that topic.")

            except wikipedia.exceptions.PageError:
                speak("I could not find information about that topic.")

            except Exception:
                speak("Sorry, I could not retrieve the information.")

    elif "search" in query:

        search_query = query.replace("search", "").strip()

        if search_query:

            speak(f"Searching Google for {search_query}.")

            webbrowser.open(
                "https://www.google.com/search?q="
                + search_query.replace(" ", "+")
            )

    elif (
    "goodbye" in query
    or "bye" in query
    or "exit" in query
    or "stop" in query
    ):

        speak("Goodbye! Have a great day.")
        return False

    else:
        speak(
            "I can help with time, date, websites, "
            "Wikipedia information, and Google searches."
        )

    return True


# --------------------------------------------------
# Main Program
# --------------------------------------------------

def main():

    speak(
        "Hello! I am your AI voice assistant. "
        "How can I help you?"
    )

    running = True

    while running:

        query = listen()

        if query:
            running = process_command(query)


# --------------------------------------------------
# Run Assistant
# --------------------------------------------------

if __name__ == "__main__":
    main()