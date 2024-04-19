from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import os
import pandas as pd
import nltk
from bs4 import BeautifulSoup
import re

# Download NLTK data including the stopwords corpus
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Function to read all the files in the directory and combine them into a single string
def read_files(directory):
    combined_text = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                combined_text += f.read()
    return combined_text

# Preprocessing function to clean text
def preprocess_text(text):
    # Remove HTML tags
    text = BeautifulSoup(text, "html.parser").get_text()
    # Remove non-alphabetic characters
    text = re.sub(r'[^a-zA-Z]', ' ', text)
    # Convert to lowercase and tokenize
    words = nltk.word_tokenize(text.lower())
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    return ' '.join(words)

# Read all the files in the 'Output_Blogs_Google' directory
combined_text = read_files("Output_Blogs_Google")

# Preprocess the text
processed_text = preprocess_text(combined_text)

# Tokenize the text into documents
documents = nltk.sent_tokenize(processed_text)

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
tfidf_data = tfidf_vectorizer.fit_transform(documents)

# Train the LDA model
lda = LatentDirichletAllocation(n_components=10, random_state=0)
lda.fit(tfidf_data)

# Print the topics found by the LDA model
print("Topics found via LDA:")
words = tfidf_vectorizer.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    print(f"Topic {i}:")
    print(" ".join([words[j] for j in topic.argsort()[-10:]]))
    print()
