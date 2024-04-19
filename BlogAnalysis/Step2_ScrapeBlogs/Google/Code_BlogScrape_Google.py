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

# Check if the stopwords corpus is available, if not, download it
nltk.download('stopwords')

# Check if the punkt tokenizer is available, if not, download it
nltk.download('punkt')

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
    body_text = "\n".join([str(p.text) for p in body])

    # Save content to text file
    save_to_text(link, title, body_text)

    # Extract top keywords
    top_keywords = get_top_keywords(body_text)

    # Save top keywords to Excel file
    save_to_excel(link, title, top_keywords)

def save_to_text(link, title, body_text):
    category = link.split("/")[5]
    directory = f"Output_Blogs_Google/{category}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    text_file_path = f"{directory}/{title}.txt"
    with open(text_file_path, "w") as text_file:
        text_file.write(body_text)
    print(f"Content for {title} saved to {text_file_path}")

def save_to_excel(link, title, top_keywords):
    df = pd.DataFrame(list(top_keywords.items()), columns=['Keyword', 'Frequency'])
    category = link.split("/")[5]
    directory = f"Output_Blogs_Google/{category}"
    if not os.path.exists(directory):
        os.makedirs(directory)
    excel_file_path = f"{directory}/{title}_keywords.xlsx"
    df.to_excel(excel_file_path, index=False)
    print(f"Top keywords for {title} saved to {excel_file_path}")

def consolidated_process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])
    return body

# Load and process the data
with open("Output_URL_Google.json", "r") as file:
    data = json.load(file)

data = list(set(data))

output_folder_name = "Output_Blogs_Google"

if not os.path.exists(output_folder_name):
    os.makedirs(output_folder_name)

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
excel_file_path = f"{output_folder_name}/Output_Words_Google.xlsx"
df.to_excel(excel_file_path, index=False)
print(f"Top 100 keywords for all blogs consolidated together saved to {excel_file_path}")
