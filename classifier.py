import json
import os
import boto3
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

# Define S3 bucket and paths
BUCKET_NAME = 'assisthive'
MODEL_KEY = 'model.pkl'
VECTORIZER_KEY = 'vectorizer.pkl'

# Define local paths in /tmp
MODEL_LOCAL_PATH = '/tmp/model.pkl'
VECTORIZER_LOCAL_PATH = '/tmp/vectorizer.pkl'

# Initialize S3 client
s3_client = boto3.client('s3')

def load_model():
    if not os.path.exists(MODEL_LOCAL_PATH):
        s3_client.download_file(BUCKET_NAME, MODEL_KEY, MODEL_LOCAL_PATH)
    if not os.path.exists(VECTORIZER_LOCAL_PATH):
        s3_client.download_file(BUCKET_NAME, VECTORIZER_KEY, VECTORIZER_LOCAL_PATH)

    with open(MODEL_LOCAL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(VECTORIZER_LOCAL_PATH, 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    
    return model, vectorizer

# Load the model and vectorizer during the first invocation
model, vectorizer = load_model()

def lambda_handler(event, context):
    try:
        # Get the preprocessed text from the event
        preprocessed_text = event['preprocessed_text']
        
        # Transform the preprocessed text using the vectorizer
        text_vector = vectorizer.transform([preprocessed_text])
        
        # Predict the service and get the prediction probabilities
        prediction = model.predict(text_vector)[0]
        prediction_proba = model.predict_proba(text_vector)[0]
        classes = model.classes_
        confidence = {classes[i]: prediction_proba[i] for i in range(len(classes))}
        
        # Determine the department based on the predicted service
        department = 'customer_support' if prediction in ['billing', 'account'] else 'technical_support'
        
        # Return the prediction and confidence scores
        return {
            'statusCode': 200,
            'body': json.dumps({
                'predicted_service': prediction,
                'department': department,
                'confidence': confidence
            })
        }
    except Exception as e:
        # Return any errors that occur
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
