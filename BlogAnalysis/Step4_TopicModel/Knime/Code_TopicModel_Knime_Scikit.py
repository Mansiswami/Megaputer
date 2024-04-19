#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:05:15 2024

@author: gautham
"""

from sklearn.feature_extraction.text import CountVectorizer
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

# Read all the files in the 'knime' directory
combined_text = read_files("/Users/gautham/Desktop/knime")

# Tokenize the text and remove stopwords
stop_words = set(stopwords.words('english'))
texts = [" ".join([word for word in document.lower().split() if word not in stop_words]) for document in combined_text.split('\n')]

# Define a predefined vocabulary
vocabulary = set(["service", "using", "spanner", "read", "google", "ai", "data", "cloud"])  # Add more words as needed

# Filter out words not present in the vocabulary
filtered_texts = []
for text in texts:
    filtered_text = " ".join(word for word in text.split() if word in vocabulary)
    filtered_texts.append(filtered_text)

# Create a CountVectorizer for parsing/counting words
count_vectorizer = CountVectorizer(stop_words='english')
count_data = count_vectorizer.fit_transform(filtered_texts)

# Train the LDA model
lda = LatentDirichletAllocation(n_components=15, random_state=0)
lda.fit(count_data)

# Print the topics found by the LDA model
print("Topics found via LDA:")
words = count_vectorizer.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    print(f"Topic {i}:")
    print(" ".join([words[j] for j in topic.argsort()[-15:]]))
    print()
