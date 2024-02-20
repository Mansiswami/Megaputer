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

    category = link.split("/")[4]

    if not os.path.exists("aws/" + category):
        os.makedirs("aws/" + category)

    try:
        with open("aws/" + category + "/" + title + ".txt", "w") as file:
            file.write(body)
    except:
        pass


with open("filtered_links_aws.json", "r") as file:
    data = json.load(file)

data = list(set(data))[30:]

if not os.path.exists("aws/"):
    os.makedirs("aws/")

# You can adjust the max_workers parameter based on your machine's capabilities
with ThreadPoolExecutor(max_workers=5) as executor:
    list(tqdm(executor.map(process_link, data), total=len(data)))
