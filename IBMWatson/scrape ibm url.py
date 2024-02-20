
import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def process_link(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string
    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])

    category = link.split("/")[5]

    directory_path = os.path.join("ibm_blogs", category)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    with open(os.path.join(directory_path, title + ".txt"), "w") as file:
        file.write(body)

with open("filtered_links_ibm_blogs.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("ibm_blogs/"):
    os.makedirs("ibm_blogs/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))
