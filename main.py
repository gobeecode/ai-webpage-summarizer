from dotenv import load_dotenv
from helpers.time_helper import TimeHelper
from helpers.url_helper import UrlHelper
from summarizer import Summarizer
from webpage import Webpage

load_dotenv()


def prompt_for_url():
    while True:
        url = input("Enter the URL of the page to summarize: ").strip().lower()
        if not UrlHelper.is_url_valid(url):
            continue
        if not UrlHelper.is_url_reachable(url):
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
            summarizer = Summarizer(platform=platform, model=model, webpage=webpage)
            print("Initializing Summarizr AI...")
            print(f"Please wait while {model} summarizes the webpage. This might take a while...")
            with TimeHelper.measure('summarize'):
                summarizer.summarize()
            elapsed = TimeHelper.get_elapsed('summarize')
            print(f"\n\n{model} summarized the webpage in {elapsed:.4f} seconds.")
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
