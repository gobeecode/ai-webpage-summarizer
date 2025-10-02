# SummarizIt
Webpage summarizer built using python and artificial intelligence.

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
- Wait for a few seconds for the summary to be retrieved.

## Configuration
- By default, the script uses llama3.2 model. 
- If you want to use other opensource models, Follow the below steps.
  - Download them using `ollama run MODEL_NAME`.
  - To view the list of all available models, Click [here](https://ollama.com/search)
    - Create a `.env` file at the root of the cloned repository.
    - Create a variable MODEL and assign the value to the name of the model you want to use.
    - For example to use gemma3 model, the .env file should have the below entry.
      ```env
        MODEL=gemma3
      ```