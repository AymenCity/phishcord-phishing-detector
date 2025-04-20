# https://medium.com/@amnahhmohammed/natural-language-processing-for-emails-9c1cf5f74f48
import imaplib
import email
import time
import requests

# login details
user_email = "aymenimap@gmail.com"
password = "ivnf yavk wonz ffjx"  # gmail app password
flask_url = "http://127.0.0.1:5000/predict"  # phishing detection API
notify_url = "http://127.0.0.1:5000/notify"

def check_inbox():
    # connect to gmail
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
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

        # Prompt: Generate Python code to send a POST request with JSON data to a Flask API and handle the response (GenAI)
        # Send to Flask API for phishing prediction
        try:
            response = requests.post(flask_url, json={"text": body})
            result = response.json().get("prediction")

            notify_data = {
                "subject": message["Subject"],
                "from": message["From"],
                "prediction": result,
                "text": body  # Include full email body for LIME
            }

            notify_response = requests.post(notify_url, json=notify_data)
            print("Frontend notified:", notify_response.status_code)

            if result == 1:
                print("This email is Phishing.")
            else:
                print("This email is Regular.")
        except Exception as e:
            print(f"Prediction error: {e}")

    imap.logout()

# Loop forever, checking inbox every 10 seconds
if __name__ == "__main__":
    print("Email phishing detector is running...")
    while True:
        try:
            check_inbox()
        except Exception as e:
            print(f"Something went wrong: {e}")
        time.sleep(10)  # Wait before next check