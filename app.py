import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Render Environment Variables से सही नाम उठाना
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'bharti_bot_123')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
PHONE_NUMBER_ID = os.environ.get('PHONE_NUMBER_ID', '1158332860694177')

@app.route('/')
def home():
    return "Bharti WhatsApp Bot is Running Perfectly!", 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    # 1. Meta Webhook Verification (GET Request)
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        
        print(f"Received Token: {token}, Expected: {VERIFY_TOKEN}")
        
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            print("WEBHOOK_VERIFIED_SUCCESSFULLY")
            return challenge, 200
        else:
            print("WEBHOOK_VERIFICATION_FAILED")
            return 'Verification failed', 403

    # 2. Incoming WhatsApp Messages (POST Request)
    elif request.method == 'POST':
        data = request.json
        print("Incoming Webhook Data:", data) # लॉग्स में देखने के लिए

        if data and data.get('object') == 'whatsapp_business_account':
            for entry in data.get('entry', []):
                for change in entry.get('changes', []):
                    value = change.get('value', {})
                    messages = value.get('messages', [])
                    
                    if messages:
                        message = messages[0]
                        from_number = message.get('from') # यूजर का नंबर
                        msg_body = message.get('text', {}).get('body', '') # यूजर का मैसेज
                        
                        print(f"Message from {from_number}: {msg_body}")
                        
                        # यहाँ से भारती बॉट का ऑटोमैटिक रिप्लाई जाएगा
                        send_whatsapp_message(from_number, f"भारती सॉफ्टवेयर में आपका स्वागत है! आपका मैसेज मिला: {msg_body}")
            
            # Flask को हमेशा एक वैलिड रिस्पॉन्स वापस देना ज़रूरी है
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
        print("Meta API Response:", response.json())
    except Exception as e:
        print("Error sending message:", str(e))
