from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
import requests
import os
import dotenv

dotenv.load_dotenv()


VAPI_AUTH_TOKEN = os.environ["AUTH_TOKEN"]
VAPI_PHONE_ID = os.environ["PHONE_ID"]
VAPI_BASE_URL = "https://api.vapi.ai"

app = Flask(__name__)
BUSINESSES = {
     'Up and Down Burger': {
          "headline": "Teleform accept orders to this local burger joint",
          "image": "up_and_down_image.png",
          'prompt': """You are a voice assistant for Up and Down Burger, a smash Burger place located at 1987 Freddy Drive, Austin, Texas. The hours are 9 AM to 5PM daily. As the first message, Hello, this is Up and Down Burger. How can I assist you today?.






Up and Down provides fresh burgers to the local Austin community.




You are tasked with answering questions about the business, and book a burger order. If they wish to book an burger order, your goal is to gather necessary information from callers in a friendly and efficient manner like follows:




1. Ask for the burger order.
2. Ask for their name for the order.
3. Request if it is pickup or drop off. If it is drop off, ask for the address of their location.
4. The Burgers cost $3.00 plus extra topping each costing $1
5. Confirm all details with the caller, including the date and time of the appointment. Please state the burger order will be ready in around 15 minutes.




- Be sure to be kind of funny and witty!
- Keep all your responses short and simple. Use casual language, phrases like "Umm...", "Well...", and "I mean" are preferred.
- This is a voice conversation, so keep your responses short, like in a real conversation. Don't ramble for too long.
""",

 
     },
     'Goomba Event Planning': {
          "headline": "Goomba accepts inquiries for event planning using Teleform",
          "image": "goomba_image.png",
          "prompt": """You are a voice assistant for Goomba Event Planning Service. As the first message, This is the Goomba Event Planning Service. How can I assist you today?


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
- This is a voice conversation, so keep your responses short, like in a real conversation. Don't ramble for too long.
"""
     },
     "Civic Complaint System": {
        "headline": "Tech City uses Teleform to run its non-emergency civic complaint system",
        "image": "civic_image.png",
        "prompt": """You are a voice assistant for Non Emergency Civic Complaint for Tech City, a hotline for non emergency lines in Tech City. As the first message, Hi, this is the Tech City Non Emergency complaint hotline. How can I assist you today?


You are tasked with answering questions about the city, and understanding complaints. Your goal is to gather necessary information from callers in a friendly and efficient manner like follows:




Examples of issues:
Report blocked driveway or illegal parking Tell us where the problem is so we can issue a citation or tow the vehicle. Request street or sidewalk cleaning Tell us where the problem is and what type of trash needs to be cleaned up. Report an abandoned vehicle Report a car, truck, or motorcycle that's been parked in one spot for more than 72 hours. Report homeless encampments Report homeless tents and other structures for removal Report a damaged or fallen tree Report problems with trees that are an urgent safety concern Report pothole and street issues Report defects in streets including potholes, missing manhole covers, or faded street markings Report graffiti issues Report graffiti on buildings, public property, and other objects Report flooding, water leaks, sewer backup, or odor issues Tell us if there are flooding, sewage backup or odor problems on the street. Report curb and sidewalk problems

Be Specific about who, what type of animal, motorcycle, or car it is. ask details.

1. Ask for their name and the issue they are dealing with
5. Confirm all details with the caller. Ask them any questions about approximate location


- Be sure to be professional and be positive!


- Keep all your responses short and simple. Use formal language, phrases like "Umm...", "Well...", and "I mean" are not preferred.
- This is a voice conversation, so keep your responses short, like in a real conversation. Don't ramble for too long."""
     }

}

call_to_user_request = {}

vapi_session = requests.Session()

vapi_session.headers.update({
    'Authorization': f'Bearer {VAPI_AUTH_TOKEN}',
    'Content-Type': 'application/json',
})

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html", businesses=BUSINESSES)

@app.route('/make_call', methods=['POST'])
def make_call():
    business = request.form['business']
    phone_number = request.form['phone']

    prompt = BUSINESSES[business]['prompt']

    response = vapi_session.post(VAPI_BASE_URL + "/call/phone", json={
        'assistant': {
            "model": {
                "provider": "openai",
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "system",
                        "content": prompt,
                    }
                ]
            },
            "voice": "jennifer-playht"
        },
        'phoneNumberId': VAPI_PHONE_ID,
        'customer': {
            'number': phone_number,
        },         
    })

    call_id = response.json()['id']

    print(f"Made a call with {call_id} to {phone_number}")

    call_to_user_request[call_id] = {
        "business": business,
        "phone": phone_number,
    }
    return redirect(url_for('call_page', call_id=call_id))

@app.route('/call')
def call_page():
    call_id = request.args.get('call_id')
    user_request = call_to_user_request.get(call_id)

    if not user_request:
        redirect(url_for('index'))

    business = user_request['business']
    phone = user_request['phone']
    return render_template('call.html', call_id=call_id, phone=phone, business=business)

@app.route('/call_status')
def get_status():
    call_id = request.args.get('call_id')

    response = vapi_session.get(VAPI_BASE_URL + "/call/" + call_id)
    call = response.json()      

    analysis = call.get("analysis", {}).get("summary") or "Waiting for call..."
        
    return {
        "status": call['status'].replace('-', " ").capitalize(),
        "transcript": call.get("transcript", "Waiting for call..."),
        "analysis": analysis,
    }


if __name__ == '__main__':
	app.run(debug=True)
