from openai import OpenAI
from io import BytesIO
from pydub import AudioSegment

def get_prompt_output(user_input):

    prompt_text = """    
    Please translate the text below from German to English:
    
    {}
    """
   
    system_prompt = '''
    You are an expert translator from German to English.
    '''

    messages = [
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": prompt_text.format(user_input)}
    ]
    
    response = openai.chat.completions.create(
        model = "gpt-3.5-turbo", # "gpt-4-1106-preview"
        messages = messages, 
        max_tokens = 1000, 
        temperature = 0
    )
    
    prompt_output = response.choices[0].message.content
    
    return(prompt_output)

with open('transcript','r') as f:
    text = f.read()

translated_text = [
    (x.split(':')[0], get_prompt_output(x.split(':')[1]))
    for x in text.split('END\n')[:-1]
]

audio_segments = []
speaker_to_voice = {'Speaker A': 'echo', 'Speaker B': 'onyx'}
openai_client = OpenAI(api_key = environ['OPENAI_API_KEY'])

for section in translated_text:
    if len(section) < 1: continue
    response = openai_client.audio.speech.create(model = "tts-1", voice = speaker_to_voice[section[0]], input = section[1])
    audio_data = BytesIO(response.content)
    audio_segment = AudioSegment.from_file(audio_data, format = "mp3")
    audio_segments.append(audio_segment)

concatenated_audio = sum(audio_segments)
concatenated_audio.export("translated_podcast.mp3", format = "mp3")
