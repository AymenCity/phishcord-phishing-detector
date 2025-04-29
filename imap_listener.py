# https://medium.com/@amnahhmohammed/natural-language-processing-for-emails-9c1cf5f74f48
# https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1 
import imaplib
import email
import time
import requests
import os
from dotenv import load_dotenv

'''
Instructions to configure email:
1. Go to .env file
2. Replace 'user_email' with your own Gmail email address
3. Replace 'password' with an App Password (not your actual password)
'''

load_dotenv()

# login details from environment variables
user_email = os.getenv("USER_EMAIL")
password = os.getenv("EMAIL_PASSWORD")

imap_server="imap.gmail.com"
flask_url ="http://127.0.0.1:5000/predict"
notify_url="http://127.0.0.1:5000/notify"
MODEL_PATH="current_model.txt"

# gets model from file
def get_current_model():
    try:
        with open(MODEL_PATH, "r") as f:
            return f.read().strip()
    except Exception as e:
        print("Error reading model file: " + str(e) + ". Falling back to 'svc_model.pkl'")
        return "svc_model.pkl"

# checks email inbox for any unseen emails
def check_inbox():
    # connect to specified imap server
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(user_email, password)

    # search for unseen emails
    imap.select('"INBOX"')
    status, messages = imap.search(None, 'UNSEEN')
    print("Checking for new emails...")

    # iterate over messages and retrieve their contents
    for num in messages[0].split():
        _, msg = imap.fetch(num, "(RFC822)")
        message = email.message_from_bytes(msg[0][1])

        # extract the email body safely
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == "text/plain":
                    content = part.get_payload(decode=True)
                    body=content.decode("utf-8")
                    break
        else:
            content = message.get_payload(decode=True)
            body=content.decode("utf-8")

        # print the message details
        print("Subject:", message["Subject"])
        print("From:", message["From"])
        print("Date:", message["Date"])
        print("Body:",body)

        selected_model = get_current_model()

        # sends to Flask API for phishing prediction
        try:
            response = requests.post(flask_url, json={"text": body})
            result = response.json().get("prediction")

            notify_data = {
                "subject": message["Subject"],
                "from": message["From"],
                "prediction": result,
                "text": body,  # Include full email body for LIME
                "selected_model": selected_model
            }

            notify_response = requests.post(notify_url, json=notify_data)
            print("Frontend notified:", notify_response.status_code)

            if result == 1:
                print("This email is Phishing.")
            else:
                print("This email is Regular.")
        except Exception as e:
            print("Prediction error: " + str(e))

    imap.logout()

# loops forever, checking inbox every 5 seconds
if __name__ == "__main__":
    print("Email phishing detector is running...")
    while True:
        try:
            check_inbox()
        except Exception as e:
            print("Something went wrong: " + str(e))
        time.sleep(5) 