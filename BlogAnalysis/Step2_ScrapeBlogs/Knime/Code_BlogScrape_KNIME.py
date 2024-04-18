#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 16:04:51 2024

@author: gautham
"""

from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora, models
from bs4 import BeautifulSoup
import os
import pandas as pd
import nltk
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

# Read all the files in the 'knime' directory on the desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
knime_directory = os.path.join(desktop_path, "knime")
combined_text = read_files(knime_directory)

# Preprocess the text: remove non-alphanumeric characters and convert to lowercase
cleaned_text = re.sub(r'[^a-zA-Z\s]', '', combined_text)
cleaned_text = cleaned_text.lower()

# Tokenize the text and remove stopwords
stop_words = set(stopwords.words('english'))
tokens = nltk.word_tokenize(cleaned_text)
filtered_tokens = [word for word in tokens if word not in stop_words]

# Create a bag-of-words representation
bow_corpus = [filtered_tokens]

# Create a dictionary representation of the documents
dictionary = corpora.Dictionary(bow_corpus)

# Convert the dictionary into a bag-of-words corpus
corpus = [dictionary.doc2bow(text) for text in bow_corpus]

# Train the LDA model with 15 topics
num_topics = 15
lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary)

# Print the topics found by the LDA model
print("Topics found via LDA:")
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic {idx}: {topic}")
