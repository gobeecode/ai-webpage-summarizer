import requests
from bs4 import BeautifulSoup


class Webpage:
    def __init__(self, url: str):
        self.url = url
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title if soup.title else "Title not found"
        irrelevant_tags = ["script", "style", "img", "input"]
        for tag in soup.body(irrelevant_tags):
            tag.decompose()
        self.text = soup.body.get_text(strip=True)

