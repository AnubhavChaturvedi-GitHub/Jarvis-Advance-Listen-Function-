import speech_recognition as sr
import os
from mtranslate import translate
from playsound import playsound
import threading

def translation_hin_to_eng(text):
    english_translation = translate(text, 'en-in')
    return english_translation

def listen():
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = False
    recognizer.energy_threshold = 35000  # Adjust this threshold based on your environment

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening....", end='', flush=True)
        try:
            audio = recognizer.listen(source, timeout=None)

            def rectext(audio):
                global translated_text# Pass 'audio' as an argument
                print("\rRecognizing...   ", end='', flush=True)
                recognized_text = recognizer.recognize_google(audio).lower()
                if recognized_text:
                    translated_text = translation_hin_to_eng(recognized_text)
                    print("\rMr.Stank: " + translated_text)
                    return translated_text

            play_sound_thread = threading.Thread(target=playsound, args=(r"F:\J.A.R.V.I.S\DATA\SOUND\system_online_bleep.mp3",))
            rec_thread = threading.Thread(target=rectext, args=(audio,))  # Pass 'audio' as an argument
            play_sound_thread.start()
            rec_thread.start()

            play_sound_thread.join()
            rec_thread.join()
            return translated_text

        except sr.UnknownValueError:
            return ""  # Set recognized_text to an empty string in case of error
        finally:
            print("\r", end='', flush=True)  # Erase "Listening...." and "Recognizing..."
            os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console after recognition

def LISTEN():
    result = {"text": ""}  # Using a dictionary to store the result

    def store_result():
        result["text"] = listen()

    play_sound_thread = threading.Thread(target=playsound, args=(r"F:\J.A.R.V.I.S\DATA\SOUND\wake.mp3",))
    listen_thread = threading.Thread(target=store_result)

    # Start both threads
    play_sound_thread.start()
    listen_thread.start()

    # Wait for both threads to finish
    play_sound_thread.join()
    listen_thread.join()

    return result["text"] or ""  # Return an empty string if result is None


