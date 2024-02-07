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

    # Extract top keywords
    top_keywords = get_top_keywords(body)

    # Save top keywords to Excel file
    save_to_excel(link, title, top_keywords)

def save_to_excel(link, title, top_keywords):
    df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
    category = link.split("/")[5]
    excel_file_path = f"google/{category}/{title}_keywords.xlsx"
    df.to_excel(excel_file_path, index=False)
    print(f"Top keywords for {title} saved to {excel_file_path}")

# Load and process the data
with open("filtered_links_google.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("google/"):
    os.makedirs("google/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))
