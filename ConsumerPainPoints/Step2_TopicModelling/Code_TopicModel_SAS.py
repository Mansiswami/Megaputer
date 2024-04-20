#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 02:38:00 2024

@author: shubhisri0809
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Function to preprocess text
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

# Function to read Excel file
def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path)
        print("File read successfully:", file_path)
        return df
    except Exception as e:
        print("Error reading file:", e)
        return None

# Read the Excel file
file_path = '/Users/shubhisri0809/Desktop/SAS Pain Points Review G2.xlsx'
df = read_excel_file(file_path)

# Check if DataFrame was successfully loaded
if df is not None:
    # Preprocess the text column
    df['Processed_Text'] = df['Dislikes'].apply(preprocess_text)

    # Vectorize the text
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    tfidf = tfidf_vectorizer.fit_transform(df['Processed_Text'])

    # Define and fit the LDA model
    lda = LatentDirichletAllocation(n_components=15, random_state=42)
    lda.fit(tfidf)

    # Function to print top words for each topic
    def print_top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([feature_names[i]
                                for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)

    # Print the top words for each topic
    print("\nTopics found via LDA:")
    tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
    print_top_words(lda, tfidf_feature_names, 10)