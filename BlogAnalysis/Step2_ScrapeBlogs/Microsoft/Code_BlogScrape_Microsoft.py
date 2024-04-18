import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import re

def clean_title(title):
    # Remove invalid characters from the title
    return re.sub(r'[\/:*?"<>|]', '', title)

def process_link(link):
    try:
        response = requests.get(link)
        response.raise_for_status()  # Check for HTTP errors
       
        soup = BeautifulSoup(response.text, "html.parser")
        title = clean_title(soup.title.string)
        body = soup.find_all("p")
        body = "\n".join([str(p.text) for p in body])

        # Check if there are enough elements in the split result
        link_parts = link.split("/")
        if len(link_parts) > 7:
            category = link_parts[7]

            if not os.path.exists("azure.microsoft/" + category):
                os.makedirs("azure.microsoft/" + category)

            with open("azure.microsoft/" + category + "/" + title + ".txt", "w", encoding="utf-8") as file:
                file.write(body)
        else:
            print(f"Skipping link: {link} - Not enough parts in the split result.")
    except requests.exceptions.RequestException as req_error:
        print(f"Request error for link {link}: {req_error}")
    except Exception as e:
        print(f"Error processing link {link}: {str(e)}")

with open("filtered_links_microsoft1.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("azure.microsoft/"):
    os.makedirs("azure.microsoft/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))
