import os

import ollama
import openai
from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

load_dotenv()


class WebpageSummarizer:
    def __init__(self, url: str):
        self.model = os.getenv("MODEL")
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
            raise ValueError("OPENAI_API_KEY not found in environment config file. Make sure it is configured correctly")
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
        messages = self.get_summarize_messages()
        response = ollama.chat(model=self.model, messages=messages)
        print(response['message']['content'])


if __name__ == '__main__':
    webpage_summarizer = WebpageSummarizer("https://zapsolv.com")
    webpage_summarizer.summarize_with_ollama()
