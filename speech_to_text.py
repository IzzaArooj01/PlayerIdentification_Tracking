import os
import requests
import time
from secret_key import API_KEY_ASSEMBLYAI

# # Load environment variables
# load_dotenv()

# AssemblyAI API key

HEADERS = {"authorization": API_KEY_ASSEMBLYAI}

# Upload audio to AssemblyAI
def upload_audio(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.assemblyai.com/v2/upload",
            headers=HEADERS,
            files={"file": f},
        )
    response.raise_for_status()
    return response.json()["upload_url"]

# Transcribe audio with speaker diarization and language support
def transcribe_audio(audio_url, language_code, enable_speaker_labels):
    request_payload = {
        "audio_url": audio_url,
        "language_code": language_code,
        "speaker_labels": enable_speaker_labels,
    }

    response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers=HEADERS,
        json=request_payload,
    )
    response.raise_for_status()
    return response.json()

# Get transcription result
def get_transcription(transcript_id):
    response = requests.get(
        f"https://api.assemblyai.com/v2/transcript/{transcript_id}",
        headers=HEADERS,
    )
    response.raise_for_status()
    return response.json()

# Main function to execute the process
def main(audio_file_path, language_code, enable_speaker_labels=False):
    # Upload the audio file
    try:
        audio_url = upload_audio(audio_file_path)
        print("Audio uploaded successfully! URL:", audio_url)
        
        # Transcribe the audio file
        transcription_response = transcribe_audio(audio_url, language_code, enable_speaker_labels)
        transcript_id = transcription_response["id"]
        print(f"Transcription started. Transcript ID: {transcript_id}")

        # Poll for transcription result
        status = "queued"
        print("Polling for transcription result. Please wait...")
        
        while status not in ["completed", "failed"]:
            time.sleep(5)  # Wait 5 seconds before polling again
            result = get_transcription(transcript_id)
            print("here")
            status = result.get("status", "failed")

        if status == "completed":
            print("**Transcription Completed!**")

            # Check for and display speaker diarization if enabled
            if enable_speaker_labels and "utterances" in result:
                print("**Speaker Diarization:**")
                for utterance in result["utterances"]:
                    start_time = utterance.get("start", 0) / 1000  # Convert milliseconds to seconds
                    end_time = utterance.get("end", 0) / 1000
                    print(f"Speaker {utterance.get('speaker', 'Unknown')} - "
                          f"[{start_time:.2f}s to {end_time:.2f}s]: {utterance.get('text', '')}")
            else:
                # Display the transcription text with timestamps for each word
                print("**Transcribed Text with Timestamps:**")
                print(result.get("text", ""))

                for word in result.get("words", []):
                    start_time = word.get("start", 0) / 1000  # Convert milliseconds to seconds
                    end_time = word.get("end", 0) / 1000
                    print(f"{word['text']} - Start: {start_time:.2f}s, End: {end_time:.2f}s")

            # Optionally, you can save the transcription to a file
            with open("transcription_with_timestamps.txt", "w") as f:
                f.write(result.get("text", ""))
            print("Transcription saved to 'transcription.txt'")

        elif status == "failed":
            print("Transcription failed. Please try again.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Replace with the path to your audio file
    audio_file_path = "../input_videos/t2.mp4"
    
    # Set desired language code and speaker diarization flag
    language_code = "es"  # Choose from 'en', 'hi', 'es', etc.
    enable_speaker_labels = False# Set to True to enable speaker diarization
    
    main(audio_file_path, language_code, enable_speaker_labels)
     