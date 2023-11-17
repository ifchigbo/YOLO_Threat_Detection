import vonage
from settings import ACCOUNT_KEY, AUTH_SEC, NUMBER_TO

def send_message(message):
    client = vonage.Client(key=ACCOUNT_KEY, secret=AUTH_SEC)
    sms = vonage.Sms(client)
    response = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": NUMBER_TO,
            "text": message
        }
    )

    if response["messages"][0]["status"] == "0":
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {response['messages'][0]['error-text']}")

send_message('Hello World')