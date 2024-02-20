import requests
from bs4 import BeautifulSoup
import json
import os
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
import time


def process_link(link):
    time.sleep(1)
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string

    # check if title is in English
    if not title.isascii():
        return

    body = soup.find_all("p")
    body = "\n".join([str(p.text) for p in body])

    try:
        with open("sas/" + title + ".txt", "w") as file:
            file.write(body)
    except:
        pass


with open("filtered_links_sas.json", "r") as file:
    data = json.load(file)

data = list(set(data))

if not os.path.exists("sas/"):
    os.makedirs("sas/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))
