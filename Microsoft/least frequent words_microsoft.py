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

# Download stopwords and punkt tokenizer
nltk.download('stopwords', download_dir=nltk_data_dir)
nltk.download('punkt', download_dir=nltk_data_dir)

# Check if the stopwords corpus is available, if not, download it
if not os.path.exists(os.path.join(nltk_data_dir, "corpora/stopwords")):
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Check if the punkt tokenizer is available, if not, download it
if not os.path.exists(os.path.join(nltk_data_dir, "tokenizers/punkt")):
    nltk.download('punkt', download_dir=nltk_data_dir)

def clean_title(title):
    # Remove invalid characters from the title
    return re.sub(r'[\/:*?"<>|]', '', title)

def get_least_frequent_keywords(text, top_n=100):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(words)
    least_frequent_keywords = dict(word_freq.most_common()[:-top_n-1:-1])
    return least_frequent_keywords

def process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = clean_title(soup.title.string)
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])

    # Extract least frequent keywords
    least_frequent_keywords = get_least_frequent_keywords(body)

    # Save least frequent keywords to Excel file
    try:
        save_to_excel(link, title, least_frequent_keywords)
    except FileNotFoundError as e:
        print(f"Skipping link: {link} - {e}")

def save_to_excel(link, title, least_frequent_keywords):
    df = pd.DataFrame(list(least_frequent_keywords.items()), columns=['Keyword', 'Frequency'])
    category = link.split("/")[5]
    directory_path = f"C:/Documents/Purdue and Anthrop document/Spring Mod 1/Megaputer/{category}/"
    
    # Create the directory if it does not exist
    os.makedirs(directory_path, exist_ok=True)

    # Save least frequent keywords to Excel file
    excel_file_path = os.path.join(directory_path, f"{title}_least_frequent_keywords.xlsx")

    try:
        df.to_excel(excel_file_path, index=False)
        print(f"Least frequent keywords for {title} saved to {excel_file_path}")
    except PermissionError as e:
        print(f"Skipping link: {link} - {e}")

def consolidated_process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])
    return body

# Load and process the data
with open("filtered_links_microsoft1.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("C:/Documents/Purdue and Anthrop document/Spring Mod 1/Megaputer/"):
    os.makedirs("C:/Documents/Purdue and Anthrop document/Spring Mod 1/Megaputer/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))

# Accumulate text from all blogs
consolidated_text = ""
for link in data:
    blog_text = consolidated_process_link(link)
    consolidated_text += blog_text

# Extract least frequent keywords from consolidated text
least_frequent_keywords = get_least_frequent_keywords(consolidated_text, top_n=100)

# Save least frequent keywords to Excel file
df = pd.DataFrame(list(least_frequent_keywords.items()), columns=['Keyword', 'Frequency'])
excel_file_path = "C:/Documents/Purdue and Anthrop document/Spring Mod 1/Megaputer/consolidated_least_frequent_keywords_top100.xlsx"
df.to_excel(excel_file_path, index=False)
print(f"Top 100 least frequent keywords for all blogs consolidated together saved to {excel_file_path}")
