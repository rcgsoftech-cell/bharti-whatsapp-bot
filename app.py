import os
from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Render ke Environment Variables se values load hongi
VERIFY_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN', 'bharti_bot_123')
ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN')
PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '1158332860694177')

@app.route('/webhook', methods=['GET'])
def verify_webhook():
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if mode == 'subscribe' and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge, 200
    else:
        return 'Verification failed', 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming webhook:", json.dumps(data, indent=2))
    
    try:
        if data and 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        value = change.get('value', {})
                        
                        if 'messages' in value and value['messages']:
                            for message in value['messages']:
                                from_number = message.get('from')
                                
                                if message.get('type') == 'text' and 'text' in message:
                                    user_text = message['text'].get('body', '')
                                    
                                    reply_text = f"Aapne likha: {user_text}. Mai Bharti Bot hun!"
                                    print(f"Sending reply to {from_number}...")
                                    send_whatsapp_message(from_number, reply_text)
                                    
    except Exception as e:
        print("Error processing webhook:", e)
    
    return 'OK', 200

def send_whatsapp_message(to, text):
    if not ACCESS_TOKEN:
        print("Error: ACCESS_TOKEN missing in Environment Variables!")
        return None
        
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages" 
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text", 
        "text": {"body": text}
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload)
        print("Sent reply Status Code:", res.status_code)
        print("Sent reply Response JSON:", res.json())
        return res.json()
    except Exception as e:
        print("Error sending message:", e)
        return None

@app.route('/')
def home():
    return 'Bharti WhatsApp Bot is Running Perfectly!'

# === RENDER PORT BINDING FIX ===
if __name__ == '__main__':
    # Render dynamic PORT variable pr chalta hai, local me 10000 ya 5000 use karega
    port = int(os.environ.get("PORT", 10000))
    # Production/Render par host="0.0.0.0" hona zaruri hai
    app.run(host="0.0.0.0", port=port, debug=False)
