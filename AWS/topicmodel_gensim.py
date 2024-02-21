from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora, models
from bs4 import BeautifulSoup
import os
import pandas as pd
import nltk

# Download NLTK data including the stopwords corpus
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Function to read all the files in the directory and combine them into a single string
def read_files(directory):
    combined_text = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                combined_text += f.read()
    return combined_text

# Read all the files in the 'aws' directory
combined_text = read_files("aws")

# Tokenize the text and remove stopwords
stop_words = set(stopwords.words('english'))
texts = [[word for word in document.lower().split() if word not in stop_words] for document in combined_text.split('\n')]

# Create a dictionary representation of the documents
dictionary = corpora.Dictionary(texts)

# Convert the dictionary into a bag-of-words corpus
corpus = [dictionary.doc2bow(text) for text in texts]

# Train the LDA model
lda_model = models.LdaModel(corpus, num_topics=10, id2word=dictionary)

# Print the topics found by the LDA model
print("Topics found via LDA:")
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic {idx}: {topic}")
