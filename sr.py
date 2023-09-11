import sys
import requests
import os
import speech_recognition as sr
from datetime import datetime
from pydub import AudioSegment

def download_audio(url, output_file):
    response = requests.get(url)
    with open(output_file, 'wb') as f:
        f.write(response.content)

def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file)
    audio.export(output_file, format="wav")

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()

    # Read the audio file
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    # Perform speech recognition
    try:
        transcribed_text = recognizer.recognize_google(audio_data)
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio.")
        transcribed_text = ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        transcribed_text = ""

    return transcribed_text

def main():
    if len(sys.argv) != 2:
        print("Usage: python transcribe_audio.py <url>")
        return

    url = sys.argv[1]

    # Generate the output file name with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_audio_file = f"data/temp_audio_{timestamp}.wav"

    # Download the audio file from the URL
    download_audio(url, temp_audio_file)

    # Convert audio to WAV format
    converted_audio_file = f"data/converted_audio_{timestamp}.wav"
    convert_to_wav(temp_audio_file, converted_audio_file)

    # Transcribe the audio file
    transcribed_text = transcribe_audio(converted_audio_file)

    # Save the transcribed text to a markdown file
    output_file = f"data/transcription_{timestamp}.md"
    with open(output_file, "w") as file:
        # Add a markdown heading for the transcription
        file.write("# Transcription\n\n")

        # Write the transcribed text
        file.write(transcribed_text)

    # Remove temporary audio files
    os.remove(temp_audio_file)
    os.remove(converted_audio_file)

if __name__ == "__main__":
    main()
