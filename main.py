import os

import ollama
import openai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

load_dotenv()


class WebpageSummarizer:
    def __init__(self, url: str):
        self.model = os.getenv("MODEL") or 'llama3.2'
        if not self.model:
            raise ValueError("MODEL not found in environment config.")
        self.url = url
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title if soup.title else "Title not found"
        irrelevant_tags = ["script", "style", "img", "input"]
        for tag in soup.body(irrelevant_tags):
            tag.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

    def get_summarize_messages(self):
        system_prompt = ("You are an assistant that analyzes the contents of a website and provides a short summary, "
                         "ignoring text that might be navigation related. Respond in markdown.")
        user_prompt = (f"You are looking at a website titled {self.title}."
                       f"The contents of this website is as follows; "
                       f"Please provide a short summary of this website in markdown. "
                       f"If it includes news or announcements, then summarize these too. {self.text}")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return messages

    def summarize_with_openai(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment file. Make sure it is configured correctly")
        elif api_key[:8] != "sk-proj-":
            raise ValueError("Invalid OPENAI_API_KEY format.")
        else:
            print("API key is found.")

        messages = self.get_summarize_messages()
        response = openai.chat.completions.create(
            model=self.model,  # For example: gpt-4o-mini
            messages=messages
        )
        print(response.choices[0].message.content)

    def summarize_with_ollama(self):
        print("Initializing the summarizer...")
        messages = self.get_summarize_messages()
        print(f"Please wait for the response from {self.model}...")
        response = ollama.chat(model=self.model, messages=messages)
        print(f"Response fetched from {self.model}!")
        print(response['message']['content'])


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


def is_reachable_url(url: str) -> bool:
    try:
        response = requests.head(url, timeout=3)
        return response.status_code < 400
    except requests.RequestException:
        return False


def prompt_for_url():
    while True:
        user_input = input("Enter the URL of the page to summarize: ").strip()
        if not is_valid_url(user_input):
            print("❌ Invalid URL. Please enter a valid URL (e.g. https://example.com)")
            continue
        if not is_reachable_url(user_input):
            print("❌ Webpage in the given URL is not reachable. Retry with a different URL.")
            continue
        print(f"✅ Got valid URL: {user_input}")
        return user_input


if __name__ == '__main__':
    url = prompt_for_url()
    webpage_summarizer = WebpageSummarizer(url)
    webpage_summarizer.summarize_with_ollama()
