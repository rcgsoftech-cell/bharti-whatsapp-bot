from flask import Flask, request
import requests, os
app = Flask(__name__)
TOKEN = os.environ.get("WA_TOKEN")
PHONE_ID = os.environ.get("PHONE_ID")

@app.route('/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get("hub.verify_token") == "bharti123":
            return request.args.get("hub.challenge")
        return "Wrong Verify Token", 403

    if request.method == 'POST':
        data = request.json
        try:
            msg = data['entry'][0]['changes'][0]['value']['messages'][0]
            sender = msg['from']
            text = msg['text']['body'].lower()

            if any(word in text for word in ['hi','hello','hey','namaste']):
                reply = "Bharti Software me swagat hai 🙏\n\nHum Website & App banate hain.\n\n1. Website Cost\n2. App Cost\n3. Portfolio\n4. Call Back Request\nReply me 1,2,3 ya 4 bheje"
            elif '1' in text:
                reply = "🌐 Website Pricing:\nBusiness Site: ₹15,000+\nE-commerce: ₹35,000+\nDomain + 1yr Hosting Free\n\n50% advance par kaam start."
            elif '2' in text:
                reply = "📱 App Pricing:\nAndroid: ₹45,000+\niOS + Android: ₹80,000+\nPlay Store upload included"
            elif '3' in text:
                reply = "🚀 Hamara Kaam:\nbhartisoftware.com/work\n\n50+ Clients: Schools, Shops, Startups"
            elif '4' in text:
                reply = "Aapka number save kar liya ✅\nTeam 30 min me call karegi.\nUrgent: 7985261077"
            else:
                reply = "Samajh nahi aaya 🤔\n1,2,3 ya 4 dabao\nYa 'Hi' likho menu ke liye"

            requests.post(f"https://graph.facebook.com/v20.0/{PHONE_ID}/messages",
                headers={"Authorization": f"Bearer {TOKEN}"},
                json={"messaging_product": "whatsapp","to": sender,"text": {"body": reply}})
        except: pass
        return "OK", 200

if __name__ == '__main__':
    app.run()
