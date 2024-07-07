import random
import json
import requests

# URL of the preprocessor Lambda function
preprocessor_url = "https://70guswvc7h.execute-api.eu-north-1.amazonaws.com/default/preprocess"

# Templates for generating billing-related queries
billing_templates = [
    "There is an error in my billing statement.",
    "I was overcharged on my recent bill.",
    "My bill amount is incorrect.",
    "I have a question about my billing statement.",
    "Why was I charged extra this month?",
    "I need a detailed breakdown of my charges.",
    "There seems to be a mistake in my bill.",
    "I was billed twice for the same service.",
    "Can you explain the charges on my bill?",
    "I didn't receive my billing statement.",
    "My bill is higher than expected.",
    "I want to dispute a charge on my bill.",
    "Can you clarify a charge on my billing statement?",
    "I need help understanding my bill.",
    "I was charged for a service I didn't use.",
    "There is a late fee on my bill that I don't understand.",
    "My bill doesn't match my usage.",
    "I want to set up a payment plan for my bill.",
    "I was charged for a service I canceled.",
    "I need to update my billing address.",
    "Why is my bill so high this month?",
    "Can I get a refund for an incorrect charge?",
    "My billing statement is missing.",
    "I need an itemized bill for my records.",
    "I have a billing issue with my account.",
    "My bill is showing an overdue amount.",
    "I want to change my billing cycle.",
    "Can you send me a copy of my last bill?",
]

# Function to generate additional billing-related data
def generate_billing_data(num_samples):
    billing_data = []
    for _ in range(num_samples):
        text = random.choice(billing_templates)
        entry = {
            "service": "billing",
            "department": "customer_support",
            "text": text
        }
        billing_data.append(entry)
    return billing_data

# Generate 100 billing-related data samples
additional_billing_data = generate_billing_data(100)

# Combine with your existing sample data
sample_data = [
    {"service": "internet_service", "department": "customer_support", "text": "I am experiencing connectivity issues with my internet service."},
    {"service": "billing", "department": "customer_support", "text": "There is an error in my billing statement."},
    {"service": "mobile_service", "department": "technical_support", "text": "My mobile connection is not working."},
    {"service": "tv_service", "department": "technical_support", "text": "The TV service is showing no signal."},
    {"service": "account", "department": "customer_support", "text": "My account is locked."},
    {"service": "internet_service", "department": "technical_support", "text": "My internet speed is very slow."},
    {"service": "billing", "department": "customer_support", "text": "I was overcharged for my service this month."},
    {"service": "mobile_service", "department": "customer_support", "text": "I need help setting up my new mobile phone."},
    {"service": "tv_service", "department": "customer_support", "text": "How do I record a show on my TV service?"},
    {"service": "account", "department": "technical_support", "text": "I can't reset my account password."},
    {"service": "internet_service", "department": "customer_support", "text": "How can I upgrade my internet plan?"},
    {"service": "billing", "department": "customer_support", "text": "I did not receive my billing statement this month."},
    {"service": "mobile_service", "department": "technical_support", "text": "My mobile data is not working."},
    {"service": "tv_service", "department": "technical_support", "text": "I am unable to access on-demand content."},
    {"service": "account", "department": "customer_support", "text": "I need to update my contact information."},
    {"service": "internet_service", "department": "technical_support", "text": "I am facing frequent disconnections with my internet."},
    {"service": "billing", "department": "customer_support", "text": "I want to change my billing address."},
    {"service": "mobile_service", "department": "customer_support", "text": "I need assistance with international roaming."},
    {"service": "tv_service", "department": "technical_support", "text": "The sound on my TV service is not working."},
    {"service": "account", "department": "technical_support", "text": "I am unable to verify my email address."},
    {"service": "internet_service", "department": "customer_support", "text": "How do I check my internet usage?"},
    {"service": "billing", "department": "customer_support", "text": "I want to enroll in paperless billing."},
    {"service": "mobile_service", "department": "technical_support", "text": "I am unable to send text messages."},
    {"service": "tv_service", "department": "customer_support", "text": "How do I access premium channels?"},
    {"service": "account", "department": "customer_support", "text": "How do I close my account?"}
]

# Add the additional billing data to the sample data
sample_data.extend(additional_billing_data)

# Function to call the preprocessor and insert data into the database
def insert_sample_data(data):
    for entry in data:
        print(f"Sending data: {entry}")  # Debugging line to print the data being sent
        response = requests.post(preprocessor_url, json=entry)
        if response.status_code == 200:
            print(f"Successfully inserted: {entry}")
        else:
            print(f"Failed to insert: {entry}. Error: {response.text}")

# Insert the sample data
insert_sample_data(sample_data)
