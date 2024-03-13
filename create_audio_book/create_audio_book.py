from pathlib import Path
from openai import OpenAI
from sys import exit
from os import system, environ
from pydub import AudioSegment
from io import BytesIO
from apify_client import ApifyClient
from pdfminer.high_level import extract_text

def extract_pdf_text_router(source, router = 'url'):
    '''
    router: Recognized values are either url or file
    '''
    
    router_mapping = {'url': extract_pdf_text_from_url, 'file': extract_pdf_text_from_file}
    payload = router_mapping[router](source)
    
    return(payload)

def extract_pdf_text_from_url(source):
    '''
    Most of this code comes from the PDF Text Extractor actor on Apify:

    https://apify.com/jirimoravcik/pdf-text-extractor

    To get it from scratch, when logged in look to the right of the actor's page
    for the API dropdown. Click that, then click Clients, and then Python.
    '''
    
    apify_client = ApifyClient(environ['APIFY_API'])
    
    run_input = {
        "urls": [source],
        "performChunking": False,
        "chunkSize": 1000,
        "chunkOverlap": 0,
    }
    
    run = apify_client.actor("QbKEOrw6PkLcy4Xms").call(run_input = run_input)
    
    text = '\n\n'.join([
        item['text'] 
        for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items()
    ])
    
    return(text)

def extract_pdf_text_from_file(source):

    text = extract_text(source)
    
    return(text)

def generate_audio(text):

    openai_client = OpenAI(api_key = environ['OPENAI_API_KEY'])
    
    sentences = text.split('.')
    audio_segments = []
    
    for i, sentence in enumerate(sentences):
        if len(sentence) < 1: continue
        response = openai_client.audio.speech.create(model = "tts-1", voice = "alloy", input = sentence)
        audio_data = BytesIO(response.content)
        audio_segment = AudioSegment.from_file(audio_data, format = "mp3")
        audio_segments.append(audio_segment)
    
    concatenated_audio = sum(audio_segments)
    concatenated_audio.export("audio_book.mp3", format = "mp3")
    
    return(True)

PDF_URL_OR_FILE_PATH = "https://www.maths.ed.ac.uk/~v1ranick/papers/wigner.pdf"
ROUTER = 'url' # or 'file' for a local file

text = extract_pdf_text_router(PDF_URL_OR_FILE_PATH, ROUTER)
generate_audio(text) # The file will be saved as audio_book.mp3 in your home directory

