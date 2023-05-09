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
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                # {"role": "system", "content": "You are a Jupyter Notebook code assistant for data scientists."},
                {"role": "user", "content": "I will supply prompts as markdown text. Please generate code based on the prompts."},
                {"role": "assistant",
                    "content": "Sure, I'm ready to generate code based on your prompts. Please feel free to provide the prompts and any additional details or requirements you might have."},
                {"role": "user", "content": "Please only provide the generated code in your answer. Do not include any other text"},
                {"role": "assistant",
                    "content": "Understood, I will only provide the generated code in my answers. Please provide the prompts and any additional details or requirements you might have."},
                {"role": "user",
                    "content": prompt}
            ]
        )
    except:
        return "Failed to generate using GPT. Please try again."
    try:
        message_string = response.choices[0].message.content
        # print(message_string)
        # json_string = re.search(
        #     "{(\r\n|\r|\n|.)*\"code\":(\r\n|\r|\n|.)*\"explanation\":(\r\n|\r|\n|.)*}", message_string).group()
        json_string = re.sub("```.*\n*", "", message_string)
        # print(json_string)
        json_dict = json.loads(json_string)
        code = json_dict["code"]
        # explanation = json_dict["explanation"]
        return code
    except:
        return message_string


# message_string = "```python\n# Check the data\nMR_df.head()\n\ndef convert_label(label):\n    if label == 'pos':\n        return 1.0 \n    elif label == 'neg':\n        return 0.0\n    else: \n        return label\n\nMR_df['y'] = MR_df['label'].apply(convert_label)\n\nassert callable(convert_label)\n```"

# regex = "```.*\n*"

# # json_string = re.search(
# #     regex, message_string).group()
# # print(json_string)

# replaced_string = re.sub(regex, "", message_string)
# print(replaced_string)

problems = read_problems()
num_samples = 1
samples = []

upper = 499
lower = 500

for task_id in problems:
    if upper < int(task_id.split("/")[1]) <= lower:
        print(f"\n{task_id}")
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
write_jsonl(f"samples_{upper}_{lower}.jsonl", samples)
