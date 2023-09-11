import sys
import os
import openai
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def download_audio(url, output_file):
    response = requests.get(url)
    with open(output_file, 'wb') as f:
        f.write(response.content)

def transcribe_audio(audio_file):
    # with open(audio_file, "rb") as audio_file_obj:
    #     transcript = openai.Audio.transcribe("whisper-1", audio_file_obj)
    audio_file = open(audio_file, 'rb')
    transcript = openai.Audio.transcribe('whisper-1', audio_file)

    return transcript["text"]

def save_transcribed_text_to_markdown(transcribed_text):
    # Generate the output file name with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"data/transcription_{timestamp}.md"

    # Format the transcribed text as markdown
    formatted_text = f"# Transcription\n\n{transcribed_text}"

    # Save the formatted text to a markdown file
    with open(output_file, "w") as file:
        file.write(formatted_text)

    return output_file

def main():
    if len(sys.argv) != 2:
        print("Usage: python transcribe_audio.py <audio_url>")
        return

    # Replace 'YOUR_API_KEY' with your actual OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    audio_url = sys.argv[1]
    audio_file_path = "data/temp_audio.m4a"

    try:
        # Download the audio file from the URL
        print(f"Downloading file from {audio_url}")
        download_audio(audio_url, audio_file_path)

        # Transcribe the audio file
        transcribed_text = transcribe_audio(audio_file_path)

        # Save the transcribed text to a markdown file
        output_file = save_transcribed_text_to_markdown(transcribed_text)
        print(f"Transcribed text saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Remove the temporary audio file
    # os.remove(audio_file_path)

if __name__ == "__main__":
    main()
