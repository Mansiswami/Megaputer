

import requests
from bs4 import BeautifulSoup
import json
import os
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import re

# Set nltk data directory explicitly
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_dir)

# Check if the stopwords corpus is available, if not, download it
if not os.path.exists(os.path.join(nltk_data_dir, "corpora/stopwords")):
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Check if the punkt tokenizer is available, if not, download it
if not os.path.exists(os.path.join(nltk_data_dir, "tokenizers/punkt")):
    nltk.download('punkt', download_dir=nltk_data_dir)

def get_top_keywords(text, top_n=100):
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

    # Sanitize the title for file name
    title = re.sub(r'[\\/*?:"<>|]', '', title)[:240]  # Limit the length of the title if necessary

    # Extract top keywords
    top_keywords = get_top_keywords(body)

    # Save top keywords to Excel file
    save_to_excel(link, title, top_keywords)

def save_to_excel(link, title, top_keywords):
    df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
    category = link.split("/")[5]
    directory_path = f"ibm_blogs/{category}"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    excel_file_path = f"{directory_path}/{title}_keywords.xlsx"
    df.to_excel(excel_file_path, index=False)
    print(f"Top keywords for {title} saved to {excel_file_path}")

def consolidated_process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])
    return body

# Load and process the data
with open("filtered_links_ibm_blogs.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("ibm_blogs/"):
    os.makedirs("ibm_blogs/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))

# Extract and accumulate text from all blogs
consolidated_text = ""
for link in data:
    blog_text = consolidated_process_link(link)
    consolidated_text += blog_text

# Extract top keywords from consolidated text
top_keywords = get_top_keywords(consolidated_text, top_n=100)

# Save top keywords to Excel file
consolidated_df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
consolidated_excel_file_path = "ibm_blogs/consolidated_keywords_top100.xlsx"
consolidated_df.to_excel(consolidated_excel_file_path, index=False)
print(f"Top 100 keywords for all blogs consolidated together saved to {consolidated_excel_file_path}")
