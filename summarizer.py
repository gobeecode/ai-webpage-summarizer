import ollama
import openai

from helpers.credential_helper import CredentialHelper
from webpage import Webpage


class Summarizer:
    def __init__(self, platform: str, model: str, webpage: Webpage):
        self.model = model
        self.text = webpage.text

    def get_summarize_messages(self):
        system_prompt = ("You are an assistant that analyzes the text and provides a short summary, "
                         "ignoring text that might be navigation related. Respond in markdown.")
        user_prompt = (f"You should provide a short summary of this content in markdown. "
                       f"If it includes news or announcements, then summarize these too. "
                       f"The contents to be summarized given as below. "
                       f"{self.text}")
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        return messages

    def summarize(self):
        print(f"Please wait while {model} summarizes the webpage. This might take a while...")
        with TimeHelper.measure('summarize'):
            messages = self.get_summarize_messages()
            if self.platform == 'openai':
                CredentialHelper.validate_openai_api_key()
                response = openai.chat.completions.create(
                    model=self.model,  # For example: gpt-4o-mini
                    messages=messages
                )
                print(f"\n\n{response.choices[0].message.content}")
            else:
                response = ollama.chat(model=self.model, messages=messages)
                print(f"\n\n{response['message']['content']}")
            elapsed = TimeHelper.get_elapsed('summarize')
            print(f"✅ Summarized the webpage using {model} in {elapsed:.4f} seconds.")


