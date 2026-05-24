import os
from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Render ke Environment Variables se uthayega
# Agar local test kar rahe ho to direct string daal sakte ho
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN', 'bharti_bot_123')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', 'EAALUXJHmDzABRsB0NxE5Kds9UdBUop3aWuWnfLZCgYxJLyJEO97IodOMejsLn7ZBKXj9sIJvyRXVcdx5vbXDlVaLKZCi2HZABZBPFrin2Mpe8V3EPtteztRPls9PKHBNpqr0CzMxD3IFIDp6Fj9fZCYmUCZCKnHbat6tYcOhlXxNtLOVb1QtenEX1KVF3tEyt0ZCdj26oRQPq4g3opKJ3li7fQAZCle1BwRR0WInFV2ZC6PGuZAM6LhpSgSeLGtLIqixzUI8zBSXaaUvh1yYlZAD5blkZC0v4uf4DQfaK2QZDZD')
PHONE_NUMBER_ID = os.environ.get('PHONE_NUMBER_ID', '1158332860694177')

# 1. Webhook verify karne ke liye - GET route Zaroori hai
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

# 2. Message aane par reply bhejne ke liye - POST route
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Incoming webhook:", json.dumps(data, indent=2))
    
    try:
        if data.get('entry'):
            for entry in data['entry']:
                for change in entry['changes']:
                    value = change['value']
                    if value.get('messages'):
                        for message in value['messages']:
                            from_number = message['from'] # +917985261077
                            
                            # Sirf text message handle karo
                            if message.get('type') == 'text':
                                user_text = message['text']['body'] # "hi"
                                
                                # Yaha reply bhejo
                                reply_text = f"Aapne likha: {user_text}. Mai Bharti Bot hun!"
                                send_whatsapp_message(from_number, reply_text)
                                
    except Exception as e:
        print("Error processing webhook:", e)
    
    return 'OK', 200

def send_whatsapp_message(to, text):
    # URL fix kiya hai - https:// double nahi hai
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
    
    res = requests.post(url, headers=headers, json=payload)
    print("Sent reply:", res.status_code, res.json())
    return res.json()

# Health check ke liye
@app.route('/')
def home():
    return 'Bharti WhatsApp Bot is Running!'

if __name__ == '__main__':
    app.run(debug=True)
