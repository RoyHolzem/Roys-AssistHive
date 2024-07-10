import random
import json
import requests

# URL of the preprocessor Lambda function
preprocessor_url = "https://70guswvc7h.execute-api.eu-north-1.amazonaws.com/default/preprocess"

# Templates for generating mobile-related queries
mobile_templates = [
    "My mobile connection is not working.",
    "I need help setting up my new mobile phone.",
    "My mobile data is not working.",
    "I am unable to send text messages.",
    "I need assistance with international roaming.",
    "My mobile phone battery drains quickly.",
    "I am having trouble connecting to Wi-Fi on my mobile.",
    "My mobile phone is overheating.",
    "I can't receive calls on my mobile phone.",
    "I need help transferring data to my new mobile phone.",
    "My mobile phone screen is frozen.",
    "I am unable to update my mobile phone software.",
    "I can't access the internet on my mobile phone.",
    "My mobile phone is running very slow.",
    "I need help setting up my email on my mobile phone.",
    "I can't hear the other person during calls on my mobile phone.",
    "My mobile phone keeps restarting on its own.",
    "I need help with mobile app installation.",
    "I can't connect my mobile phone to Bluetooth devices.",
    "My mobile phone camera is not working."
]

# Function to generate additional mobile-related data
def generate_mobile_data(num_samples):
    mobile_data = []
    for _ in range(num_samples):
        text = random.choice(mobile_templates)
        entry = {
            "service": "mobile_service",
            "department": "technical_support",
            "text": text
        }
        mobile_data.append(entry)
    return mobile_data

# Generate 100 mobile-related data samples
additional_mobile_data = generate_mobile_data(100)

# Function to call the preprocessor and insert data into the database
def insert_sample_data(data):
    for entry in data:
        print(f"Sending data: {entry}")  # Debugging line to print the data being sent
        response = requests.post(preprocessor_url, json=entry)
        if response.status_code == 200:
            print(f"Successfully inserted: {entry}")
        else:
            print(f"Failed to insert: {entry}. Error: {response.text}")

# Insert the mobile-related sample data
insert_sample_data(additional_mobile_data)
