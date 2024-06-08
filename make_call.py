import os
import dotenv
from twilio.rest import Client

dotenv.load_dotenv()

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

call = client.calls.create(
  url="http://demo.twilio.com/docs/voice.xml",
  to=os.environ["MY_PHONE_NUMBER"],
  from_="+17076222056"
)

print(call.sid)