import sys
import requests
from google.cloud import speech_v1p1beta1 as speech
from datetime import datetime

def download_audio(url, output_file):
    response = requests.get(url)
    with open(output_file, 'wb') as f:
        f.write(response.content)

def transcribe_audio(audio_file):
    client = speech.SpeechClient()

    with open(audio_file, "rb") as audio_file_obj:
        content = audio_file_obj.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcribed_text = ""
    for result in response.results:
        transcribed_text += result.alternatives[0].transcript + " "

    return transcribed_text

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

    audio_url = sys.argv[1]
    audio_file_path = "data/temp_audio.wav"

    try:
        # Download the audio file from the URL
        download_audio(audio_url, audio_file_path)

        # Transcribe the audio file
        transcribed_text = transcribe_audio(audio_file_path)

        # Save the transcribed text to a markdown file
        output_file = save_transcribed_text_to_markdown(transcribed_text)
        print(f"Transcribed text saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Remove the temporary audio file
    import os
    os.remove(audio_file_path)

if __name__ == "__main__":
    main()
