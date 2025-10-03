# Summarizr AI
Webpage summarizer developed using python and artificial intelligence.

## Installation
- Download and install Ollama application.
- Pull a model from ollama using the below command.
  ```shell
    ollama run llama3.2
    ```
- Clone the repo and change directory to the root of the repo.
- Upgrade pip
  ```shell
    python -m pip install --upgrade pip
  ```
- Run the below command to install all the dependencies.
  ```shell
    pip install -r requirements.txt
  ```

## Usage
- Execute the below command in the commandline.
  ```shell
    python ./main.py
  ```
- Enter the url of the webpage to be summarized.
- Enter the platform name to be used for summarization. Default: ollama. Supported: ollama, openai.
- Enter the model to use for summarization. Default: llama3.2
- Wait for a few seconds for the summary to be retrieved.

## Configuration
- By default, the script uses llama3.2 model in ollama platform. 
- If you want to use other opensource models, Follow the below steps.
  - Download them using `ollama run MODEL_NAME`.
  - To view the list of all available models, Click [here](https://ollama.com/search)
  - Enter the model name to use, when the script prompts for the model name.