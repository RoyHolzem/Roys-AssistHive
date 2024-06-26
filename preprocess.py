import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import pandas as pd
from sqlalchemy import create_engine
import os

# Download necessary NLTK data
nltk.download('stopwords')
nltk.download('wordnet')

# Initialize NLP tools
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\W', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    words = [lemmatizer.lemmatize(stemmer.stem(word)) for word in words if word not in stop_words]
    return ' '.join(words)

# Lambda handler function
def lambda_handler(event, context):
    body = json.loads(event['body'])
    customer_text = body['customer_text']
    service = body['service']
    department = body['department']

    # Preprocess text
    cleaned_text = preprocess_text(customer_text)
    
    # Store in SQL database
    engine = create_engine(os.getenv('DATABASE_URL'))
    df = pd.DataFrame({
        'customer_text': [customer_text],
        'cleaned_text': [cleaned_text],
        'service': [service],
        'department': [department]
    })
    df.to_sql('customer_data', con=engine, if_exists='append', index=False)

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Data processed and stored successfully'})
    }
