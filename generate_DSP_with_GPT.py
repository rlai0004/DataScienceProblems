import openai
import os
import re
import time
import json
from dotenv import load_dotenv
from data_science_problems.read import read_problems
from data_science_problems.utils import write_jsonl

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_code(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Jupyter Notebook code assistant for data scientists."},
            {"role": "user", "content": "I will supply prompts as markdown text. Please generate code based on the prompts."},
            {"role": "assistant",
                "content": "Sure, I'd be happy to help! Please provide me with the first prompt."},
            {"role": "user", "content": "Please give your generated code and explanations in JSON format like this: {\"code\": <your code here>, \"explanation\": <your explanation here>}."},
            {"role": "assistant",
                "content": "Understood, I'll provide the code and explanations in JSON format as requested. Let's get started!"},
            {"role": "user",
                "content": prompt}
        ]
    )
    try:
        message_string = response.choices[0].message.content
        # print(message_string)
        json_string = re.search(
            "{(\r\n|\r|\n|.)*\"code\":(\r\n|\r|\n|.)*\"explanation\":(\r\n|\r|\n|.)*}", message_string).group()
        # print(json_string)
        json_dict = json.loads(json_string)
        code = json_dict["code"]
        # explanation = json_dict["explanation"]
        return code
    except:
        return message_string


problems = read_problems()
num_samples = 1
samples = []
for task_id in problems:
    if int(task_id.split("/")[1]) < 500:
        for _ in range(num_samples):
            completion = ""
            try:
                completion = generate_code(problems[task_id]["prompt"])
            except:  # handle any exceptions raised by the generate_code function
                completion = 'Failed to extract the code snippet'
            # samples.append(dict(task_id=task_id, prompt=problems[task_id]["prompt"], completion=completion, test=problems[task_id]["test"]))
            # only return the task_id and the completion
            samples.append(dict(task_id=task_id, completion=completion))
            # if len(samples) % 3 == 0:  # wait for 1 minute every 3 requests
            #     time.sleep(60)
write_jsonl("samples.jsonl", samples)
