import os
import time

import ollama
import openai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

load_dotenv()


class WebpageSummarizer:
    def __init__(self, url: str, model: str):
        self.url = url
        self.model = model
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
        print(f"\n\n{response.choices[0].message.content}")

    def summarize_with_ollama(self):
        messages = self.get_summarize_messages()
        response = ollama.chat(model=self.model, messages=messages)
        print(f"\n\n{response['message']['content']}")


def is_url_valid(url: str) -> bool:
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


def is_url_reachable(url: str) -> bool:
    try:
        response = requests.head(url, timeout=3)
        return response.status_code < 400
    except requests.RequestException:
        return False


def prompt_for_url():
    while True:
        url = input("Enter the URL of the page to summarize: ").strip().lower()
        if not is_url_valid(url):
            print("❌ Invalid URL. Please enter a valid URL (e.g. https://example.com)")
            continue
        if not is_url_reachable(url):
            print("❌ Webpage in the given URL is not reachable. Retry with a different URL.")
            continue
        print(f"✅ Selected URL: {url}")
        return url


def prompt_for_platform():
    while True:
        platform = input("Enter the platform name: (Default: ollama. Supported: ollama, openai) ").strip().lower()
        if not platform:
            platform = 'ollama'
        if platform not in ['ollama', 'openai']:
            print("❌ Invalid platform. Please enter a valid platform name.")
            continue
        print(f"✅ Selected platform: {platform}")
        return platform


def prompt_for_model(platform: str):
    while True:
        if platform == 'openai':
            model = input("Enter the model name (Default: gpt-4o-mini): ").strip().lower()
            if not model:
                model = 'gpt-4o-mini'
        elif platform == 'ollama':
            model = input("Enter the model name (Default: llama3.2): ").strip().lower()
            if not model:
                model = 'llama3.2'
        else:
            print(f"❌ Unsupported platform {platform}. Please select a valid platform.")
            continue
        print(f"✅ Selected model: {model}")
        return model


def main():
    while True:
        try:
            url = prompt_for_url()
            platform = prompt_for_platform()
            model = prompt_for_model(platform)
            webpage_summarizer = WebpageSummarizer(url, model)
            print("Initializing SummarizeIt...")
            print(f"Please wait while {model} summarizes the webpage. This might take a while...")
            start = time.time()
            if platform == 'openai':
                webpage_summarizer.summarize_with_openai()
            else:
                webpage_summarizer.summarize_with_ollama()
            end = time.time()
            # Calculate elapsed time in seconds
            elapsed_seconds = end - start
            print(f"\n\n{model} summarized the webpage in {elapsed_seconds:.4f} seconds.")
        except Exception as e:
            print(f"❌ Failed to summarize the webpage. Exception: {e}")
            retry = input("Do you want to retry? (Y/n): ").strip().lower()
            if not retry:
                retry = 'y'
            if retry == 'y':
                continue
            else:
                break
    print("👋 Exiting SummarizIt. Goodbye!")


if __name__ == '__main__':
    main()
