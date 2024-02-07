import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('stopwords')
nltk.download('punkt')

def get_top_keywords(text, top_n=10):
    # Tokenize the text
    words = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]

    # Get word frequencies
    word_freq = Counter(words)

    # Get top N keywords
    top_keywords = word_freq.most_common(top_n)

    return top_keywords

def process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])

    category = link.split("/")[5]

    if not os.path.exists("google/" + category):
        os.makedirs("google/" + category)

    with open("google/" + category + "/" + title + ".txt", "w") as file:
        file.write(body)

    # Extract top keywords and print them
    top_keywords = get_top_keywords(body)
    print(f"Top keywords for {title}: {top_keywords}")

with open("filtered_links_google.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("google/"):
    os.makedirs("google/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))
