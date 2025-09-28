# test_bot_locally.py
import requests
import os

# The URL where your bot is running
BOT_URL = "http://127.0.0.1:5000/whatsapp"

# A fake phone number to simulate a user session
FAKE_FROM_NUMBER = "whatsapp:+1234567890"

def send_message(message):
    """Simulates sending a WhatsApp message to your bot."""
    payload = {
        "From": FAKE_FROM_NUMBER,
        "Body": message
    }
    try:
        response = requests.post(BOT_URL, data=payload)
        response.raise_for_status() # Raise an exception for bad status codes
        
        # Twilio expects an XML response (TwiML), so we print the text content
        print(f"\n[BOT's TwiML RESPONSE]:\n{response.text}\n")
        
    except requests.exceptions.RequestException as e:
        print(f"\n--- ERROR ---")
        print(f"Could not connect to the bot server at {BOT_URL}.")
        print("Please ensure your 'bot.py' Flask application is running in another terminal.")
        print(f"Error details: {e}")

def main():
    print("--- Local DBT Chatbot Tester ---")
    print("Type your message and press Enter.")
    print("Type 'quit' to exit.")
    print("--------------------------------")

    # This simulates the first "welcome" message from Twilio
    send_message("") 

    while True:
        user_input = input("[YOU]: ")
        if user_input.lower() == 'quit':
            break
        send_message(user_input)

if __name__ == "__main__":
    main()