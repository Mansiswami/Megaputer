#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 01:59:17 2024

@author: mansiswami
"""

import requests
from bs4 import BeautifulSoup
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Set nltk data directory explicitly
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_dir)

# Check if the stopwords corpus is available, if not, download it
if not os.path.exists(os.path.join(nltk_data_dir, "corpora/stopwords")):
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Check if the punkt tokenizer is available, if not, download it
if not os.path.exists(os.path.join(nltk_data_dir, "tokenizers/punkt")):
    nltk.download('punkt', download_dir=nltk_data_dir)

def get_top_keywords(text, top_n=50):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(words)
    return word_freq.most_common(top_n)

def process_link(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        body = soup.find_all("p")
        body = "\n".join([str(p.text) for p in body])
        return body
    except Exception as e:
        print(f"Error processing link {link}: {e}")
        return ''

# Load AWS URLs from blog_urls.txt
with open("blog_urls.txt", "r") as file:
    data = file.readlines()
    data = [url.strip() for url in data]

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    blog_contents = list(tqdm(executor.map(process_link, data), total=len(data)))

# Combine all blog contents into a single string
combined_text = "\n".join(blog_contents)

# Get the top 50 keywords from the combined text
top_keywords = get_top_keywords(combined_text)

# Print the top 50 keywords
print("Top 50 Keywords:")
for keyword, frequency in top_keywords:
    print(f"{keyword}: {frequency}")
