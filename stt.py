from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

client = OpenAI()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
AUDIO = os.environ["AUDIO_RE"]

audio_file= open(AUDIO, "rb")
transcription = client.audio.transcriptions.create(
  model="whisper-1", 
  file=audio_file,
  response_format="text"
)
print(transcription)