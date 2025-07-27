import json
import smtplib
import time
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def load_notification_config():
    with open("config.json", "r") as file:
        return json.load(file)

def send_email_alert(location, recipient_email):
    msg = MIMEMultipart()
    msg["From"] = "dcpe2a01devops.grp5.notifsys@gmail.com"
    msg["To"] = recipient_email
    msg["Subject"] = "🔥 FIRE ALERT!"

    body = f"URGENT: Fire detected at {location}. Immediate help required!"
    msg.attach(MIMEText(body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("dcpe2a01devops.grp5.notifsys@gmail.com", "Dev0ps2510_Group5!")
    server.send_message(msg)
    server.quit()

def send_telegram_alert(bot_token, chat_id, location):
    message = f"🔥 FIRE ALERT!\nLocation: {location}\nImmediate help required!"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def notify_fire_alert(system_state):
    config = load_notification_config()
    sent = False

    while True:
        if system_state["fire_detected"] and not system_state["system_override"] and not sent:
            send_email_alert(config["location"], config["recipient_email"])
            send_telegram_alert(config["telegram_bot_token"], config["telegram_chat_id"], config["location"])
            sent = True
        if not system_state["fire_detected"]:
            sent = False
        time.sleep(5)
