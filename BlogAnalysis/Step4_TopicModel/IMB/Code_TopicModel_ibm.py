import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
import nltk

# Ensure NLTK stopwords are downloaded
nltk.download('stopwords')

# Load the dataset from the Excel file
file_path = '/Users/siqi/desktop/Megaputer/consolidated_keywords_top100.xlsx'
df = pd.read_excel(file_path)

# Assuming the column with keywords is named 'Keyword'
documents = df['Keyword'].tolist()

# Preprocess and vectorize the keywords for LDA using TfidfVectorizer with n-grams
stop_words = stopwords.words('english')
tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=(1, 2))  # Considering unigrams and bigrams
data_vectorized = tfidf_vectorizer.fit_transform(documents)

# Perform LDA with 15 topics
lda_model = LatentDirichletAllocation(n_components=15, random_state=0, max_iter=10, learning_decay=0.7)
lda_model.fit(data_vectorized)

# Display the topics
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic %d:" % (topic_idx))
        print(" + ".join([f'{topic[i]:.3f}*"'+feature_names[i]+'"' for i in topic.argsort()[:-no_top_words - 1:-1]]))

no_top_words = 10
display_topics(lda_model, tfidf_vectorizer.get_feature_names_out(), no_top_words)
