import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import spacy

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

# Function to preprocess text
def preprocess_text(text):
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and token.is_alpha]
    return ' '.join(tokens)

# Read the CSV file
df = pd.read_csv('/Users/gautham/Desktop/google cloud g2 reviews.csv')

# Preprocess the text column
df['Processed_Text'] = df['Dislikes'].apply(preprocess_text)

# Vectorize the text
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
tfidf = tfidf_vectorizer.fit_transform(df['Processed_Text'])

# Define and fit the LDA model with 15 topics
n_topics = 15  # Number of topics
lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
lda.fit(tfidf)

# Function to print top words for each topic
def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)

# Print the top words for each topic
print("\nTopics found via LDA with 15 topics:")
tfidf_feature_names = tfidf_vectorizer.get_feature_names_out()
print_top_words(lda, tfidf_feature_names, 10)
