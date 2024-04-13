import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim import corpora, models

# Download NLTK data including the stopwords corpus
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Function to read all the files in the directory and combine them into a single string
def read_files(directory):
    combined_text = ""
    for root, dirs, files in os.walk(directory):
        for file in files:
            with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                combined_text += f.read()
    return combined_text

# Preprocess the text
def preprocess_text(text):
    # Tokenize
    tokens = word_tokenize(text.lower())
    # Remove stopwords, non-alphabetic tokens, and tokens with length less than 3
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.isalpha() and word not in stop_words and len(word) > 2]
    # Lemmatize
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return tokens

# Read all the files in the directory
combined_text = read_files("/Users/siqi/desktop/Megaputer")

# Tokenize and preprocess the text
tokens = preprocess_text(combined_text)

# Create a bag-of-words representation
dictionary = corpora.Dictionary([tokens])
corpus = [dictionary.doc2bow(tokens)]

# Train the LDA model with 15 topics
num_topics = 15
lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary)

# Print the topics found by the LDA model
print("Top words for each topic:")
for idx, topic in lda_model.print_topics(-1):
    # Extract the words and their probabilities
    words = lda_model.show_topic(idx, topn=10)
    print(f"Topic {idx}: {', '.join([word[0] for word in words])}")
