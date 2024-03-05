from pathlib import Path
from openai import OpenAI
from sys import exit
from os import system, environ
from pydub import AudioSegment
from io import BytesIO
from apify_client import ApifyClient
from pdfminer.high_level import extract_text

apify_client = ApifyClient(environ['APIFY_API'])
openai_client = OpenAI(api_key = environ['OPENAI_API_KEY'])
PDF_URL = "https://www.maths.ed.ac.uk/~v1ranick/papers/wigner.pdf"

'''
# Use this code if the pdf is a url
'''

run_input = {
    "urls": [PDF_URL],
    "performChunking": False,
    "chunkSize": 1000,
    "chunkOverlap": 0,
}

run = apify_client.actor("QbKEOrw6PkLcy4Xms").call(run_input = run_input)

text = '\n\n'.join([
    item['text'] 
    for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items()
])

'''
# Use this code if it's local on your machine

pdf_path = ''
text = extract_text(pdf_path)
'''

sentences = text.split('.')
audio_segments = []

for i, sentence in enumerate(sentences):
    if len(sentence) < 1: continue
    response = client.audio.speech.create(model = "tts-1", voice = "alloy", input = sentence)
    audio_data = BytesIO(response.content)
    audio_segment = AudioSegment.from_file(audio_data, format = "mp3")
    audio_segments.append(audio_segment)

concatenated_audio = sum(audio_segments)
concatenated_audio.export("audio_book.mp3", format = "mp3")
