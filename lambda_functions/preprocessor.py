import json
import boto3
import nltk
import re
from nltk.corpus import stopwords

# Ensure nltk_data can find the data files
nltk.data.path.append("/opt/python/nltk_data")

# Initialize the Lambda client
lambda_client = boto3.client('lambda')

def preprocess_input(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = nltk.word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered_words)

def lambda_handler(event, context):
    text = event.get('text')

    if not text:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Text must be provided'})
        }

    # Preprocess the input text
    preprocessed_text = preprocess_input(text)

    # Invoke the classifier Lambda function
    response = lambda_client.invoke(
        FunctionName='classifier',  # Ensure this is the correct function name
        InvocationType='RequestResponse',
        Payload=json.dumps({'preprocessed_text': preprocessed_text})
    )

    response_payload = json.loads(response['Payload'].read())
    
    # Check if 'body' is in the response_payload and load the classification result
    if 'body' in response_payload:
        classification_result = json.loads(response_payload['body'])
    else:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Invalid response structure from classifier'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps({
            'original_text': text,
            'preprocessed_text': preprocessed_text,
            'classification_result': classification_result
        })
    }
