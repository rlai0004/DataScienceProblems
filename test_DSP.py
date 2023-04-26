import json


with open("samples.jsonl", "r") as f_samples:
    problems = f_samples.readlines()

for line in problems:
    problem = json.loads(line)
    print(problem["task_id"])
    # print(problem["completion"] + "\n" + problem["test"])

    try:
        exec(problem["completion"] + "\n" + problem["test"])
        passed = True
    except Exception as e:
        passed = False
        print(e)

    print("Outcome:", passed)

