import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer

# Function to load the model and vectorizer from disk
def load_model():
    with open('model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('vectorizer.pkl', 'rb') as vectorizer_file:
        vectorizer = pickle.load(vectorizer_file)
    return model, vectorizer

# Function to preprocess the input text
def preprocess_input(text):
    text = text.lower()  # Convert text to lowercase
    text = re.sub(r'\W', ' ', text)  # Remove non-word characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

# Function to predict the service category and provide confidence score
def predict_service(text):
    model, vectorizer = load_model()
    processed_text = preprocess_input(text)
    text_vector = vectorizer.transform([processed_text])
    
    # Get prediction and confidence
    prediction = model.predict(text_vector)[0]
    prediction_proba = model.predict_proba(text_vector)[0]
    
    # Map prediction probability to class labels
    classes = model.classes_
    confidence = {classes[i]: prediction_proba[i] for i in range(len(classes))}
    
    return prediction, confidence

# Tester
if __name__ == "__main__":
    input_text = "my phone doesnt work i cant get no calls"
    print(f"Input text: {input_text}")
    
    predicted_service, confidence = predict_service(input_text)
    print(f"The predicted service category is: {predicted_service}")
    
    print("Confidence scores:")
    for service, score in confidence.items():
        print(f"  {service}: {score:.4f}")
