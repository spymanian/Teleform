from openai import OpenAI
import os
import dotenv

dotenv.load_dotenv()

client = OpenAI()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="hello, i am here to assist you!",

) as response:
    response.stream_to_file("output.mp3")