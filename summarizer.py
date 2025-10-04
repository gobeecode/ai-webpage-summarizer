import os
import ollama
import openai


class Summarizer:
    def __init__(self, text: str, model: str):
        self.model = model
        self.text = text

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
