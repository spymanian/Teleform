import requests
import time
import json
import dotenv
import os
import argparse

dotenv.load_dotenv()

# Your Vapi API Authorization token
auth_token = os.environ["AUTH_TOKEN"]
# The Phone Number ID, and the Customer details for the call
phone_number_id = os.environ["PHONE_ID"]

parser = argparse.ArgumentParser(description="Collect info over the phone using AI.")
parser.add_argument("phone_number", type=str, help="Customer phone number with country code, e.g., +1234567890")
args = parser.parse_args()

customer_number = args.phone_number
print(f"Customer phone number: {customer_number}")

headers = {
    'Authorization': f'Bearer {auth_token}',
    'Content-Type': 'application/json',
}

data = {
    'assistant': {
        "model": {
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": """You are a voice assistant for Goomba Event Planning Service. As the first message, This is the Goomba Event Planning Service. How can I assist you today?


You are tasked with answering questions about the event that the caller wants to have, and understand about . If they wish to book an event, your goal is to gather necessary information from callers in a friendly and efficient manner like follows:




1. Ask for their name and the event they want us to plan for them
2. Estimated Date for this event
3. What Supplies and arrangements for the event
4.Ask how many Total number of guests
5. What area do you want the venue to be in?
6. Ask for their Email for a Quotation
7. Confirm all details with the caller. Ask them any questions about approximate location


- Be sure to be professional and be positive!
- Keep all your responses short and simple. Use formal language, phrases like "Umm...", "Well...", and "I mean" are not preferred.
- This is a voice conversation, so keep your responses short, like in a real conversation. Don't ramble for too long."""


                }
            ]
        },
        "voice": "jennifer-playht"
    },
    'phoneNumberId': phone_number_id,
    'customer': {
        'number': customer_number,
    },
}

# Make the POST request to Vapi to create the phone call
response = requests.post(
    'https://api.vapi.ai/call/phone', headers=headers, json=data)

response.raise_for_status()
call = response.json()
print(call['id'])

url = "https://api.vapi.ai/call/" + call['id']
while(response.json()['status'] != 'ended'):
    time.sleep(5)
    response = requests.request("GET", url, headers=headers)
    print(response.json()['status'])

if (response.json()['status'] == 'ended'):
    print(json.dumps(response.json(), indent=2))