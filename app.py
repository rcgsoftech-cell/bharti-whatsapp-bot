import requests

ACCESS_TOKEN = "EAALUXJHmDzABRsB0NxE5Kds9UdBUop3aWuWnfLZCgYxJLyJEO97IodOMejsLn7ZBKXj9sIJvyRXVcdx5vbXDlVaLKZCi2HZABZBPFrin2Mpe8V3EPtteztRPls9PKHBNpqr0CzMxD3IFIDp6Fj9fZCYmUCZCKnHbat6tYcOhlXxNtLOVb1QtenEX1KVF3tEyt0ZCdj26oRQPq4g3opKJ3li7fQAZCle1BwRR0WInFV2ZC6PGuZAM6LhpSgSeLGtLIqixzUI8zBSXaaUvh1yYlZAD5blkZC0v4uf4DQfaK2QZDZD" # apna token
PHONE_NUMBER_ID = "1158332860694177" # test number ki ID

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    # Check karo message aaya ya nahi
    if data.get('entry'):
        for entry in data['entry']:
            for change in entry['changes']:
                value = change['value']
                if value.get('messages'):
                    for message in value['messages']:
                        from_number = message['from'] # +917985261077
                        user_text = message['text']['body'] # "hi"
                        
                        # Yaha reply bhejo
                        reply_text = f"Aapne likha: {user_text}. Mai Bharti Bot hun!"
                        send_whatsapp_message(from_number, reply_text)
    
    return 'OK', 200

def send_whatsapp_message(to, text):
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
    print("Sent reply:", res.json())
