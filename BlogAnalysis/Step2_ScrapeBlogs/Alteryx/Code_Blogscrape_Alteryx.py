import requests
from bs4 import BeautifulSoup
import json
import os
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Function to process each link
def process_link(link):
    print("Processing link:", link)  # Add this line for debugging
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(link, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string
        body = soup.find_all("p")
        body = "\n".join([str(p.text) for p in body])

        # Update this part based on the URL structure
        category = link.split("/")[-1]  # Get the last part of the URL

        if not os.path.exists("alteryx/" + category):
            os.makedirs("alteryx/" + category)

        with open("alteryx/" + category + "/" + title + ".txt", "w") as file:
            file.write(body)
    except Exception as e:
        print("Failed to fetch content from {}. Error: {}".format(link, str(e)))

# Load links from filtered_links_alteryx.json
with open("filtered_links_alteryx.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("alteryx/"):
    os.makedirs("alteryx/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    for link in tqdm(data):
        executor.submit(process_link, link)
        time.sleep(1)  # Add a delay between requests to avoid overwhelming the server
