import pandas as pd

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

import joblib
import os

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    
    tokens = word_tokenize(text)
    
    stop_words = set(stopwords.words('russian')+stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    
    return ' '.join(tokens)


MODEL_PATH = 'toxicity_model.joblib'
VECTORIZER_PATH = 'vectorizer.joblib'

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    data = pd.read_csv("./labeled.csv")
    
    X = data['comment'].apply(preprocess)
    y = data['toxic']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(random_state=42)
    model.fit(X_train_vec, y_train)
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)
else:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

def predict_toxic(text):
    processed_text = preprocess(text)
    text_vec = vectorizer.transform([processed_text])
    prediction = model.predict_proba(text_vec)[0]
    return prediction[1]

while True:
    text = input(">")
    toxicity = predict_toxic(text)
    print(f"Вероятность: {toxicity:.2%}")