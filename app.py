import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Render Environment Variables के सही नाम
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'bharti_bot_123')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.environ.get('PHONE_NUMBER_ID', '1158332860694177')

@app.route('/')
def home():
    return "Bharti WhatsApp Bot is Running Perfectly!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Meta Webhook Verification (GET)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Verification failed', 403

    # 2. Incoming WhatsApp Messages (POST)
    elif request.method == 'POST':
        data = request.json
        print("Incoming Data:", data)

        if data and data.get('object') == 'whatsapp_business_account':
            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    messages = value.get('messages', [])
                    
                    if messages:
                        message = messages[0]
                        from_number = message.get('from')
                        msg_body = message.get('text', {}).get('body', '')
                        
                        # यहाँ से भारती बॉट का ऑटोमैटिक रिप्लाई ट्रिगर होगा
                        send_whatsapp_message(from_number, f"भारती सॉफ्टवेयर में आपका स्वागत है! आपका मैसेज मिला: {msg_body}")
            
            # Flask को हमेशा 200 रिस्पॉन्स वापस देना ज़रूरी है
            return 'EVENT_RECEIVED', 200
        
        return 'Not a valid WhatsApp Event', 200

def send_whatsapp_message(to_number, text_content):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": text_content}
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print("Meta Response:", response.json())
    except Exception as e:
        print("Error:", str(e))
