import logging
import pandas as pd
import pymysql
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Database credentials
rds_host = "customerdata.c9aoqc44eckn.us-east-1.rds.amazonaws.com"
db_username = "admin"
db_password = "mypassword"
db_name = "customerdata"

# Setup logging
logging.basicConfig(filename='training.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Function to fetch data from the database
def fetch_data():
    try:
        connection = pymysql.connect(
            host=rds_host,
            user=db_username,
            password=db_password,
            database=db_name,
            connect_timeout=5
        )
        
        query = "SELECT cleaned_text, service FROM customerdata"
        data = pd.read_sql(query, connection)
        logging.info("Successfully fetched data from database.")
        
    except pymysql.MySQLError as e:
        logging.error(f"Error fetching data: {e}")
        return None
    finally:
        if 'connection' in locals():
            connection.close()
        
    return data

# Preprocess data function
def preprocess_data(data):
    # Assuming 'cleaned_text' is already preprocessed and stored as text
    return data

# Main function to train the model
def train_model():
    # Fetch and preprocess data
    data = fetch_data()
    if data is None:
        logging.error("Failed to fetch data.")
        print("Failed to fetch data.")
        return
    
    data = preprocess_data(data)
    
    # Feature extraction using TF-IDF
    vectorizer = TfidfVectorizer(max_df=0.8, min_df=5, max_features=1000)
    X = vectorizer.fit_transform(data['cleaned_text'])
    logging.info(f"Vectorized data shape: {X.shape}")  # Log vectorized data shape
    
    # Use 'service' as the target variable
    y = data['service']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a logistic regression model
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    logging.info("Accuracy: %.2f", accuracy_score(y_test, y_pred))
    logging.info("Classification Report:\n %s", classification_report(y_test, y_pred))
    
    # Save the model and vectorizer
    with open('model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    with open('vectorizer.pkl', 'wb') as vectorizer_file:
        pickle.dump(vectorizer, vectorizer_file)
    
    logging.info("Model trained and saved successfully.")

# Run the function to train the model
if __name__ == "__main__":
    train_model()
