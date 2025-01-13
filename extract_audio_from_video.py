import subprocess
import wave
import json
from vosk import Model, KaldiRecognizer

# Extract audio from video using ffmpeg
def extract_audio_from_video(video_file, audio_file):
    command = f"ffmpeg -i {video_file} -vn -acodec pcm_s16le -ar 16000 -ac 1 {audio_file}"
    subprocess.run(command, shell=True)

# Perform word-level speech recognition and get timestamps
def transcribe_audio_with_timestamps(audio_file, model_path="path_to_vosk_model"):
    model = Model(model_path)  # Load Vosk model
    wf = wave.open(audio_file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    
    words_with_timestamps = []
    
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            for word in result["result"]:
                words_with_timestamps.append({
                    "word": word["word"],
                    "start_time": word["start"],
                    "end_time": word["end"]
                })
    
    return words_with_timestamps

# Example usage
video_file = "input_videos/elcassico.mp4"
audio_file = "match_audio.wav"
extract_audio_from_video(video_file, audio_file)

words_with_timestamps = transcribe_audio_with_timestamps(audio_file)
print(words_with_timestamps)
