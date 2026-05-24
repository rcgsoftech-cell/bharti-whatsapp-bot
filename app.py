
@app.route('/webhook', methods=['POST'])
def handle_message():
    data = request.get_json()
    print("Incoming:", data)
    
    try:
        # Message nikalna
        entry = data['entry'][0]
        changes = entry['changes'][0]
        value = changes['value']
        messages = value.get('messages')
        
        if messages:
            message = messages[0]
            from_number = message['from'] # jisne message bheja
            msg_body = message['text']['body'] # "hi" ya jo bhi bheja
            print(f"Message from {from_number}: {msg_body}")
            
            # Yaha reply bhej rahe hain
            send_reply(from_number, "Hello! Mai Bharti Bot hun. Aapne likha: " + msg_body)
            
    except Exception as e:
        print("Error:", e)
        
    return 'OK', 200

def send_reply(to_number, message_text):
    url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("Reply sent:", response.json())
