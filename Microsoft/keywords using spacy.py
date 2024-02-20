import requests
from bs4 import BeautifulSoup
import json
import os
import nltk
import spacy
from nltk.corpus import stopwords
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

# Load spaCy English language model
nlp = spacy.load("en_core_web_sm")

def clean_title(title):
    # Remove invalid characters from the title
    return re.sub(r'[\/:*?"<>|]', '', title)

def get_top_keywords(text, top_n=100):
    # Use spaCy for further text processing
    doc = nlp(text)
    
    # Filter out stop words and non-alphabetic words
    words = [token.text.lower() for token in doc if token.is_alpha and token.text.lower() not in stopwords.words('english')]
    
    # Get word frequencies
    word_freq = Counter(words)
    
    # Get top keywords
    top_keywords = dict(word_freq.most_common(top_n))
    
    return top_keywords

def process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = clean_title(soup.title.string)
    body = soup.find_all("p")
    
    # Process each paragraph individually
    consolidated_text = "\n".join([p.text for p in body])

    # Extract top keywords
    top_keywords = get_top_keywords(consolidated_text)

    # Save top keywords to Excel file
    directory_path = f"C:/Documents/Purdue and Anthrop document/Spring Mod 1/Microsoft_Spacy/"
    os.makedirs(directory_path, exist_ok=True)
    excel_file_path = os.path.join(directory_path, f"{title}_keywords.xlsx")

    try:
        df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
        df.to_excel(excel_file_path, index=False)
        print(f"Top keywords for {title} saved to {excel_file_path}")
    except PermissionError as e:
        print(f"Skipping link: {link} - {e}")

    # Return the title
    return title

# Load and process the data
with open("filtered_links_microsoft1.json", "r") as file:
    data = json.load(file)

data = list(set(data))

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))

# Accumulate text from all blogs
consolidated_text = ""
for link in data:
    blog_title = process_link(link)
    consolidated_text += blog_title + "\n"  # Add newline between blog titles

# Extract top keywords from consolidated text
top_keywords = get_top_keywords(consolidated_text, top_n=100)

# Save top keywords to Excel file
df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
excel_file_path = "C:/Documents/Purdue and Anthrop document/Spring Mod 1/Microsoft_Spacy/consolidated_keywords_top100_Spacy.xlsx"
df.to_excel(excel_file_path, index=False)
print(f"Top 100 keywords for all blogs consolidated together saved to {excel_file_path}")
