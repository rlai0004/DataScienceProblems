import openai
from dotenv import load_dotenv
import os
import re
import json

from data_science_problems.read import read_problems
from data_science_problems.utils import write_jsonl

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_code(prompt):
    # return "def get_string(x,y):\n    return str(x)+str(y)"
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
        print(message_string)
        json_string = re.search("{(\r\n|\r|\n|.)*\"code\":(\r\n|\r|\n|.)*\"explanation\":(\r\n|\r|\n|.)*}", message_string).group()
        print(json_string)
        json_dict = json.loads(json_string)
        code = json_dict["code"]
        explanation = json_dict["explanation"]
        return code
    except:
        return message_string


problems = read_problems()

# print(problems["DSP/0"])

num_samples = 1
samples = [
    # dict(task_id=task_id, completion=generate_code(problems[task_id]["prompt"]))
    dict(task_id=task_id, prompt=problems[task_id]["prompt"], completion=generate_code(problems[task_id]["prompt"]), test=problems[task_id]["test"])
    for task_id in problems
    for _ in range(num_samples)
]
write_jsonl("samples.jsonl", samples)
