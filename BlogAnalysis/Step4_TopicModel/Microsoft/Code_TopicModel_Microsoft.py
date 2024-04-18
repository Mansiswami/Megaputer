from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from bs4 import BeautifulSoup
import os
import pandas as pd
import nltk

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

# Read all the files in the 'azure.microsoft' directory
combined_text = read_files(r"C:\Users\infof\azure.microsoft")

# Tokenize the text and remove stopwords
stop_words = set(stopwords.words('english'))
texts = [" ".join([word for word in document.lower().split() if word not in stop_words]) for document in combined_text.split('\n')]

# Create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_data = tfidf_vectorizer.fit_transform(texts)

# Train the LDA model
lda = LatentDirichletAllocation(n_components=15, random_state=0)
lda.fit(tfidf_data)

# Print the topics found by the LDA model
print("Topics found via LDA:")
words = tfidf_vectorizer.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    print(f"Topic {i}:")
    print(" ".join([words[j] for j in topic.argsort()[-10:]]))
    print()
