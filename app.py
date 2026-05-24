import os
from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Render ke Environment Variables se uthayega
VERIFY_TOKEN = os.environ.get('bharti_bot_123', 'bharti_bot_123')
ACCESS_TOKEN = os.environ.get('EAALUXJHmDzABRknsh2f20qHt6FbrqNzUE80bbp3QQzsqS7dyO4OZAie29xqta2wryat1dr2VvFIPXqBNw0uJKo7TOcZBtXUQJztjSq0XhxoLmRndTFZCspXx5BOkfJHbKpeH5duLZB0H6OBo1763KknXlr29p56TQXJOqKroXQZBamZBqSEZCnAkQofflQ2YAvHgroCbRnG5N4Yz0fIdy6tV8VWvmEQLYdG3VZAoVIN61F07NJ77ZBnZA0ZAXoTc9Vm0rZAPtcOqglYYZBga6kE7tIsdJqqBwVPkJUTrzdAZDZD')
PHONE_NUMBER_ID = os.environ.get('1158332860694177')

# 1. Webhook verify karne ke liye - GET route
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
                            from_number = message['from']
                            
                            if message.get('type') == 'text':
                                user_text = message['text']['body']
                                
                                reply_text = f"Aapne likha: {user_text}. Mai Bharti Bot hun!"
                                send_whatsapp_message(from_number, reply_text)
                                
    except Exception as e:
        print("Error processing webhook:", e)
    
    return 'OK', 200

def send_whatsapp_message(to, text):
    # ✅ URL FIX: https:// double tha, hata diya
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
        print("Sent reply:", res.status_code, res.json())
        return res.json()
    except Exception as e:
        print("Error sending message:", e)
        return None

# Health check ke liye
@app.route('/')
def home():
    return 'Bharti WhatsApp Bot is Running!'

if __name__ == '__main__':
    app.run(debug=True)
