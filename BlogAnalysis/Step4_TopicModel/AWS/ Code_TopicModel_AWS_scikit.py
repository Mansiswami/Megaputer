#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 12:52:30 2024

@author: mansiswami
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
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                combined_text += f.read()
    return combined_text

# Read all the files in the 'aws' directory
combined_text = read_files("aws")

# Tokenize the text and remove stopwords
stop_words = set(stopwords.words('english'))
texts = [" ".join([word for word in document.lower().split() if word not in stop_words]) for document in combined_text.split('\n')]

# Create a CountVectorizer for parsing/counting words
count_vectorizer = CountVectorizer(stop_words='english')
count_data = count_vectorizer.fit_transform(texts)

# Train the LDA model
lda = LatentDirichletAllocation(n_components=10, random_state=0)
lda.fit(count_data)

# Print the topics found by the LDA model
print("Topics found via LDA:")
words = count_vectorizer.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    print(f"Topic {i}:")
    print(" ".join([words[j] for j in topic.argsort()[-10:]]))
    print()
