import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
import pandas as pd

nltk.download('stopwords')
nltk.download('wordnet')

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

# Example usage
data = {
    'customer_text': [
        "I can't access my internet service",
        "The billing statement is incorrect",
        "Need help with my mobile connection",
        "Technical support needed for TV service",
        "My account is locked"
    ]
}

df = pd.DataFrame(data)
df['cleaned_text'] = df['customer_text'].apply(preprocess_text)
print(df)
