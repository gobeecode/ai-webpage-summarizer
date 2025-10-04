import os
import time

import ollama
import openai
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from summarizer import Summarizer
from webpage import Webpage

load_dotenv()


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
            webpage = Webpage(url)
            text = webpage.text
            summarizer = Summarizer(model=model, text=text)
            print("Initializing Summarizr AI...")
            print(f"Please wait while {model} summarizes the webpage. This might take a while...")
            start = time.time()
            if platform == 'openai':
                summarizer.summarize_with_openai()
            else:
                summarizer.summarize_with_ollama()
            end = time.time()
            # Calculate elapsed time in seconds
            elapsed_seconds = end - start
            print(f"\n\n{model} summarized the webpage in {elapsed_seconds:.4f} seconds.")
            break
        except Exception as e:
            print(f"❌ Failed to summarize the webpage. Exception: {e}")
            retry = input("Do you want to retry? (Y/n): ").strip().lower()
            if not retry:
                retry = 'y'
            if retry == 'y':
                continue
            else:
                break
        finally:
            print("Exiting Summarizr AI. Goodbye 👋")


if __name__ == '__main__':
    main()
