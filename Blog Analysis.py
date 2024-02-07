#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 18:31:56 2024

@author: gautham
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd

nltk.download('stopwords')
nltk.download('punkt')

def get_top_keywords(text, top_n=10):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(words)
    top_keywords = dict(word_freq.most_common(top_n))
    return top_keywords

def process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])
    return body

# Load and process the data
with open("filtered_links_google.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("google/"):
    os.makedirs("google/")

# Accumulate text from all blogs
consolidated_text = ""
for link in data:
    blog_text = process_link(link)
    consolidated_text += blog_text

# Extract top keywords from consolidated text
top_keywords = get_top_keywords(consolidated_text)

# Save top keywords to Excel file
df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
excel_file_path = "google/consolidated_keywords.xlsx"
df.to_excel(excel_file_path, index=False)
print(f"Top keywords for all blogs consolidated together saved to {excel_file_path}")
