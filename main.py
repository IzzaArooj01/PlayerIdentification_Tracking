import requests
from speech_to_text import *

filename = "../input_videos/elclassico.mp4"
audio_url = upload(filename)
language='spanish'

save_transcript(audio_url, 'transcription_with_timestamps.txt',language)