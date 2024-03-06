# Start by making sure the `assemblyai` package is installed.
# If not, you can install it by running the following command:
# pip install -U assemblyai
#
# Note: Some macOS users may need to use `pip3` instead of `pip`.

import assemblyai as aai
from os import environ

# Replace with your API token
aai.settings.api_key = environ['ASSEMBLYAI_API_KEY']

# URL of the file to transcribe
FILE_URL = "podcast_24580_einfach_mal_luppen_episode_1384131_80_000_sniper_fur_eine_pfeife.mp3"

# You can also transcribe a local file by passing in a file path
# FILE_URL = './path/to/file.mp3'

transcriber = aai.Transcriber()

config = aai.TranscriptionConfig(speaker_labels = True, language_code = "de")

transcript = transcriber.transcribe(
  FILE_URL,
  config = config
)

for utterance in transcript.utterances:
  
  with open('transcript', 'a') as file:
    print(f"Speaker {utterance.speaker}: {utterance.text} END", file = file)
