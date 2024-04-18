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

# Set nltk data directory explicitly
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
nltk.data.path.append(nltk_data_dir)

# Check if the stopwords corpus is available, if not, download it
if not os.path.exists(os.path.join(nltk_data_dir, "corpora/stopwords")):
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Check if the punkt tokenizer is available, if not, download it
if not os.path.exists(os.path.join(nltk_data_dir, "tokenizers/punkt")):
    nltk.download('punkt', download_dir=nltk_data_dir)

# Reload the stopwords corpus with the updated data directory
stop_words = set(stopwords.words('english'))

def get_top_keywords(text, top_n=100):
    words = word_tokenize(text.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(words)
    top_keywords = dict(word_freq.most_common(top_n))
    return top_keywords

def process_link(link):
    print("Processing link:", link)  # Debug statement to see link structure
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])

    # Extract top keywords
    top_keywords = get_top_keywords(body)

    # Save top keywords to Excel file
    save_to_excel(link, title, top_keywords)

    # Save content to text file
    save_to_text(link, title, body)

def save_to_excel(link, title, top_keywords):
    df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
    # Extract category from link (assuming different structure)
    category = link.split("/")[-1]  # Change index according to link structure
    directory_path = f"knime/{category}/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    excel_file_path = f"{directory_path}{title}_keywords.xlsx"
    df.to_excel(excel_file_path, index=False)
    print(f"Top keywords for {title} saved to {excel_file_path}")

def save_to_text(link, title, body):
    # Extract category from link (assuming different structure)
    category = link.split("/")[-1]  # Change index according to link structure
    directory_path = f"knime/{category}/"
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    text_file_path = f"{directory_path}{title}_content.txt"
    with open(text_file_path, "w", encoding="utf-8") as text_file:
        text_file.write(body)
    print(f"Content for {title} saved to {text_file_path}")

def consolidated_process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])
    return body

# Load and process the data
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
json_file_path = os.path.join(desktop_path, "knime_blog_links.json")
with open(json_file_path, "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("knime/"):
    os.makedirs("knime/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))

# Accumulate text from all blogs
consolidated_text = ""
for link in data:
    blog_text = consolidated_process_link(link)
    consolidated_text += blog_text

# Extract top keywords from consolidated text (top 100 keywords)
top_keywords = get_top_keywords(consolidated_text, top_n=100)

# Save top keywords to Excel file
df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
excel_file_path = os.path.join(desktop_path, "knime_top_100_keywords.xlsx")
df.to_excel(excel_file_path, index=False)
print(f"Top 100 keywords for all blogs consolidated together saved to {excel_file_path}")
