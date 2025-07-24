from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
CORS(app)

EMAIL_ADDRESS = "info@megaplus.ge"
EMAIL_PASSWORD = "s6MQZrmBMEF3"
SMTP_SERVER = "mail.megaplus.ge"
SMTP_PORT = 465

@app.route('/', methods=['GET'])
def arvici():
    return "Test! Works Well!", 200

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')

    if not name or not phone:
        return jsonify({"status": "error", "message": "Name and phone are required."}), 400

    msg = EmailMessage()
    msg['Subject'] = "New Contact Submission from Website"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(f"Name: {name}\nPhone: {phone}")

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return jsonify({"status": "success", "message": "Email sent!"}), 200

    except Exception as e:
        print("EMAIL ERROR:", str(e))
        return jsonify({"status": "error", "message": f"Failed to send email: {str(e)}"}), 500
