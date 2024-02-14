import os
import pandas as pd
from collections import Counter
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords
nltk.download('stopwords')

# Get English stopwords from NLTK
stop_words = set(stopwords.words('english'))

# Function to extract keywords from a text
def extract_keywords(text):
    # Split the text into words and remove punctuation
    words = text.lower().split()
    words = [word.strip('.,!?"\'') for word in words]
    
    # Remove stopwords
    words = [word for word in words if word not in stop_words]
    
    # Count the frequency of each word
    word_freq = Counter(words)
    
    # Sort the words by frequency and get the top 50
    top_keywords = word_freq.most_common(50)
    
    return top_keywords

# Function to process each blog folder
def process_blog_folder(folder_path):
    keyword_counter = Counter()
    
    # Loop through all text files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Read the content of the text file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract keywords from the content and update the keyword counter
        keywords = extract_keywords(content)
        keyword_counter.update(dict(keywords))
    
    # Convert the counter to a DataFrame
    df = pd.DataFrame(keyword_counter.most_common(50), columns=['Keyword', 'Frequency'])
    
    # Save the DataFrame to an Excel sheet
    folder_name = os.path.basename(folder_path)
    df.to_excel(f'alteryx/{folder_name}_top_keywords.xlsx', index=False)

# Process each blog folder
blog_folders = [folder for folder in os.listdir('alteryx/') if os.path.isdir(os.path.join('alteryx/', folder))]
for folder in tqdm(blog_folders):
    folder_path = os.path.join('alteryx/', folder)
    process_blog_folder(folder_path)

# Consolidate top keywords from all blogs
all_keywords_counter = Counter()
for folder in blog_folders:
    folder_path = os.path.join('alteryx/', folder)
    keyword_file_path = os.path.join(folder_path, f'{folder}_top_keywords.xlsx')
    
    # Read the top keywords Excel sheet into a DataFrame
    df = pd.read_excel(keyword_file_path)
    
    # Update the keyword counter with the top keywords from this blog
    all_keywords_counter.update(dict(zip(df['Keyword'], df['Frequency'])))

# Convert the counter to a DataFrame
all_keywords_df = pd.DataFrame(all_keywords_counter.most_common(50), columns=['Keyword', 'Total Frequency'])

# Save the consolidated top keywords to an Excel sheet
all_keywords_df.to_excel('alteryx/consolidated_keywords_top50.xlsx', index=False)
