import random
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


def parse_gpt_response(message_string):
    regex_matches = re.findall("```.*\n((.|\n)*?)\n```", message_string)
    if len(regex_matches) > 0:
        final_code_string = ""
        for match in regex_matches:
            for group in match:
                if group != "python" and len(group) > 1:
                    final_code_string += "\n" + group + "\n"
        return final_code_string
    else:
        return message_string


def generate_code_base(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "I will supply prompts. Please generate code based on the prompts."},
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
        return "Failed to generate using GPT. Please try again.", "Failed to generate using GPT. Please try again."
    try:
        message_string = response.choices[0].message.content
        # print(message_string)
        # json_string = re.search(
        #     "{(\r\n|\r|\n|.)*\"code\":(\r\n|\r|\n|.)*\"explanation\":(\r\n|\r|\n|.)*}", message_string).group()
        final_code_string = parse_gpt_response(message_string)
        # regex_matches = re.findall("```.*\n((.|\n)*?)\n```", message_string)
        # if len(regex_matches) > 0:
        #     final_code_string = ""
        #     for match in regex_matches:
        #         for group in match:
        #             if group != "python" and len(group) > 1:
        #                 final_code_string += "\n" + group + "\n"
        return final_code_string, message_string
        # else:
        #     return message_string, message_string
        # code_sections = re.findall("```.*\n(.|\n)*?\n```", message_string)
        print(code_sections)
        final_code_string = ""
        for code_section in code_sections:
            code_string = re.sub("```.*\n*", "", code_section)
            final_code_string += "\n" + code_string
        # json_string = re.sub("```.*\n*", "", message_string)
        # print(json_string)
        # json_dict = json.loads(json_string)
        # code = json_dict["code"]
        # explanation = json_dict["explanation"]
        # print(json_string)
        return final_code_string, message_string
    except:
        return message_string, message_string


def generate_code_persona(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "You are a Jupyter Notebook code assistant for data scientists."},
                {"role": "assistant",
                    "content": "Great! I'm ready to assist you with any questions or tasks related to Jupyter Notebook and data science. Just let me know how I can help!"},
                {"role": "user", "content": "I will supply prompts. Please generate code based on the prompts."},
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
        return "Failed to generate using GPT. Please try again.", "Failed to generate using GPT. Please try again."
    try:

        message_string = response.choices[0].message.content
        # print(message_string)
        # json_string = re.search(
        #     "{(\r\n|\r|\n|.)*\"code\":(\r\n|\r|\n|.)*\"explanation\":(\r\n|\r|\n|.)*}", message_string).group()
        final_code_string = parse_gpt_response(message_string)
        # message_string = response.choices[0].message.content
        # # print(message_string)
        # # json_string = re.search(
        # #     "{(\r\n|\r|\n|.)*\"code\":(\r\n|\r|\n|.)*\"explanation\":(\r\n|\r|\n|.)*}", message_string).group()
        # code_sections = re.findall("```.*\n(.|\n)*?\n```", message_string)
        # final_code_string = ""
        # for code_section in code_sections:
        #     code_string = re.sub("```.*\n*", "", code_section)
        #     final_code_string += "\n" + code_string
        # json_string = re.sub("```.*\n*", "", message_string)
        # print(json_string)
        # json_dict = json.loads(json_string)
        # code = json_dict["code"]
        # explanation = json_dict["explanation"]
        # print(json_string)
        return final_code_string, message_string
    except:
        return message_string, message_string


def generate_code_question_refinement(prompt):
    try:
        print(f"\nOriginal Prompt:")
        print(prompt)
        question_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Within the scope of generating code for a Jupyter Notebook, suggest a better version of the prompt to use instead. I will supply the original prompt in the next message."},
                {"role": "assistant",
                    "content": "Sure, I can help you come up with a better version of the prompt for generating code in a Jupyter Notebook. Please provide me with the current version of the prompt so that I can assist you in improving it."},
                {"role": "user",
                    "content": prompt}
            ]
        )
        print("Improved Prompt:")
        print(question_response.choices[0].message.content)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "I will supply prompts. Please generate code based on the prompts."},
                {"role": "assistant",
                    "content": "Sure, I'm ready to generate code based on your prompts. Please feel free to provide the prompts and any additional details or requirements you might have."},
                {"role": "user", "content": "Please only provide the generated code in your answer. Do not include any other text"},
                {"role": "assistant",
                    "content": "Understood, I will only provide the generated code in my answers. Please provide the prompts and any additional details or requirements you might have."},
                {"role": "user",
                    "content": question_response.choices[0].message.content}
            ]
        )
    except:
        return "Failed to generate using GPT. Please try again.", "Failed to generate using GPT. Please try again."
    try:
        message_string = response.choices[0].message.content
        # print(message_string)
        # json_string = re.search(
        #     "{(\r\n|\r|\n|.)*\"code\":(\r\n|\r|\n|.)*\"explanation\":(\r\n|\r|\n|.)*}", message_string).group()
        final_code_string = parse_gpt_response(message_string)
        # json_string = re.sub("```.*\n*", "", message_string)
        # print(json_string)
        # json_dict = json.loads(json_string)
        # code = json_dict["code"]
        # explanation = json_dict["explanation"]
        # print(json_string)
        return final_code_string, message_string
    except:
        return message_string, message_string


def generate_code_meta_language_creation(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "I will supply prompts. Please generate code based on the prompts."},
                {"role": "assistant",
                    "content": "Sure, I'm ready to generate code based on your prompts. Please feel free to provide the prompts and any additional details or requirements you might have."},
                {"role": "user",
                    "content": "When generating code, take into account the following definitions for Jupyter Notebook code cells in the Data Science/Machine Learning pipeline:\n\nData Collection: Data Collection cells load data that will often be passed to other stages in the notebook.\n\nData Wrangling: Data wrangling cells clean, transform, or filter data loaded from the data collection stage. These cells also perform feature engineering on the collected data.\n\nTraining: Training cells define and fit supervised-learning ML models to the collected data to predict on some feature of the data.\n\nEvaluation: Evaluation cells predict a feature of some dataset using ML model(s) or measure/compute the accuracy or explanatory power of the model(s).\n\nTraining+Evaluation: Training+Evaluation cells include both training and evaluation stages, as described above.\n\nExploration: Exploration cells visualize, print or plot data or data’s relevant information (e.g. shape) and plot or print results related to the training or evaluation process. Unsupervised learning is also classified as exploration."},
                {"role": "assistant",
                    "content": "Certainly, I'll generate code snippets based on the provided definitions for each stage in the Data Science/Machine Learning pipeline."},
                {"role": "user", "content": "Please only provide the generated code in your answer. Do not include any other text"},
                {"role": "assistant",
                    "content": "Understood, I will only provide the generated code in my answers. Please provide the prompts and any additional details or requirements you might have."},
                {"role": "user",
                    "content": prompt}
            ]
        )
    except:
        return "Failed to generate using GPT. Please try again.", "Failed to generate using GPT. Please try again."
    try:
        message_string = response.choices[0].message.content
        # print(message_string)
        # json_string = re.search(
        #     "{(\r\n|\r|\n|.)*\"code\":(\r\n|\r|\n|.)*\"explanation\":(\r\n|\r|\n|.)*}", message_string).group()
        final_code_string = parse_gpt_response(message_string)
        # regex_matches = re.findall("```.*\n((.|\n)*?)\n```", message_string)
        # if len(regex_matches) > 0:
        #     final_code_string = ""
        #     for match in regex_matches:
        #         for group in match:
        #             if group != "python" and len(group) > 1:
        #                 final_code_string += "\n" + group + "\n"
        return final_code_string, message_string
        # else:
        #     return message_string, message_string
        # code_sections = re.findall("```.*\n(.|\n)*?\n```", message_string)
        print(code_sections)
        final_code_string = ""
        for code_section in code_sections:
            code_string = re.sub("```.*\n*", "", code_section)
            final_code_string += "\n" + code_string
        # json_string = re.sub("```.*\n*", "", message_string)
        # print(json_string)
        # json_dict = json.loads(json_string)
        # code = json_dict["code"]
        # explanation = json_dict["explanation"]
        # print(json_string)
        return final_code_string, message_string
    except:
        return message_string, message_string


problems = read_problems()
num_samples = 10
samples = []

# for problem in problems:
#     if int(problem.split("/")[1]) == 1:
#         print(problems[problem]["prompt"])
#         break

for i in range(10):
    choice = problems[random.choice(list(problems.keys()))]
    print(choice["task_id"])
    print(choice["notebook_path"])
    print(choice["prompt"])

exit()


for lower in range(0, 1095, 50):
    try:
        upper = lower + 49
        for task_id in problems:
            # break
            if lower <= int(task_id.split("/")[1]) <= upper:
                print(f"\n{task_id}")
                for _ in range(num_samples):
                    completion = ""
                    try:
                        (completion, full_response) = generate_code_question_refinement(
                            problems[task_id]["prompt"])
                    except:  # handle any exceptions raised by the generate_code function
                        completion = 'Failed to extract the code snippet'
                        full_response = 'Failed to extract the code snippet'
                    print(f"\nCode Completion:")
                    print(completion)
                    # samples.append(dict(task_id=task_id, prompt=problems[task_id]["prompt"], completion=completion, test=problems[task_id]["test"]))
                    # only return the task_id and the completion
                    samples.append(
                        dict(task_id=task_id, completion=completion, full_response=full_response))
                    # if len(samples) % 10 == 0:  # wait for 1 minute every 3 requests
                    #     time.sleep(30)
        write_jsonl(f"samples_{lower}_{upper}.jsonl", samples)
    except:
        pass
    # time.sleep(60)
    # print(lower, upper)
