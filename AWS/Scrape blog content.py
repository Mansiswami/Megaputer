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
    top_keywords = dict(word_freq.most_common(top_n))
    return top_keywords

def process_link(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string if soup.title else "Unknown Title"
        category = link.split("/")[3] if len(link.split("/")) > 3 else "Unknown Category"
        body = soup.find_all("p")
        body = "\n".join([str(p.text) for p in body])

        # Extract top keywords
        top_keywords = get_top_keywords(body)

        # Save top keywords to Excel file
        save_to_excel(link, title, category, top_keywords)
    except Exception as e:
        print(f"Error processing link {link}: {e}")

def save_to_excel(link, title, category, top_keywords):
    try:
        df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
        excel_file_path = f"aws/{category}/{title}_keywords.xlsx"
        os.makedirs(os.path.dirname(excel_file_path), exist_ok=True)
        df.to_excel(excel_file_path, index=False)
        print(f"Top keywords for {title} saved to {excel_file_path}")
    except Exception as e:
        print(f"Error saving keywords for {title}: {e}")

# Load AWS URLs from blog_urls.txt
with open("blog_urls.txt", "r") as file:
    data = file.readlines()
    data = [url.strip() for url in data]

if not os.path.exists("aws/"):
    os.makedirs("aws/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))
