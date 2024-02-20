from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
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


def get_top_keywords(text, top_n=100):
    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = Counter(words)
    return word_freq.most_common(top_n)


# read all the files in the aws directory
def read_files(directory):
    combined_text = ""
    files = os.listdir(directory)
    for file in files:
        with open(directory + "/" + file, "r") as f:
            combined_text += f.read()
    return combined_text


# get the top 50 keywords from the combined text
def get_top_keywords_from_files(directory):
    combined_text = read_files(directory)
    return get_top_keywords(combined_text)


combined_text = read_files("sas")
top_keywords = get_top_keywords(combined_text)

for i, (word, freq) in enumerate(top_keywords):
    print(f"{i + 1}. {word}: {freq}")


# do topic modelling

# Create a CountVectorizer for parsing/counting words
count_vectorizer = CountVectorizer(stop_words='english')
count_data = count_vectorizer.fit_transform([combined_text])

# Create and fit the LDA model
lda = LatentDirichletAllocation(n_components=5, random_state=0)
lda.fit(count_data)

# Print the topics found by the LDA model
print("Topics found via LDA:")
words = count_vectorizer.get_feature_names_out()
for i, topic in enumerate(lda.components_):
    print(f"Topic {i}:")
    print(" ".join([words[j] for j in topic.argsort()[-10:]]))
    print()
