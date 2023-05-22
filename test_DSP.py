import json
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from collections import defaultdict
import numpy as np
from tqdm import tqdm
from data_science_problems.utils import stream_jsonl, estimate_pass_at_k, reliability_guard
import re

def evaluate(path):
    path = Path(path.strip())
    nb = nbformat.read(path, as_version=4)

    cells_json = nb["cells"]
    cells = [''.join(cell['source']) for cell in cells_json]
    for idx in range(len(cells)-1):
        if "task_id" in cells_json[idx]["metadata"]:
            task_id = cells_json[idx]["metadata"]["task_id"]
            source = cells_json[idx]["source"]
            if "#### GENERATED" in source:
#                 print(task_id)
                test = cells_json[idx+1]["outputs"]
                # if not has_no_error(test):
                    # print(f"{task_id} had an error")
                return has_no_error(test), task_id
            

def has_no_error(x):
    for element in x:
        if "ename" in element:
            return False
    return True


# reliability_guard()

out_file = "generated.txt"

with open(out_file) as f:
    ps = f.readlines()

error_file = "errors.txt"
with open(error_file, "w") as ferr:
    for line in ps:
        try:
            # notebook_filename = "juice-github-repos\mwizasimbeye11.data-science-africa-2018-abuja\data-science-africa-2018-abuja-master\PythonBasicsx.task_id.0.0.ipynb"
            notebook_filename = Path(line.strip())
            print(f"executing {notebook_filename}")
            nb = nbformat.read(notebook_filename, as_version=4)
            # print(nb)
            parent = notebook_filename.parent
            # print(parent)
            client = NotebookClient(nb, 
                timeout=10, 
                kernel_name="python3", 
                resources= {'metadata': {'path': parent}}, 
                allow_errors=True
            )
            # print(client)
            # print("trying to execute")
        # try:
            enb = client.execute()
            nbformat.write(enb, notebook_filename)
        except:
            print(notebook_filename, file=ferr)
            print(f"something went wrong with {notebook_filename}")
        # print(notebook_filename)
        # nbformat.write(enb, notebook_filename)
        # print(notebook_filename)

print("Complute pass@k for the executed notebooks.")
with open(out_file) as f:
    ps = f.readlines()

results = defaultdict(list)
for notebook_filename in tqdm(ps):
    try:
        result, task_id = evaluate(notebook_filename)
        results[task_id].append(result)
        # print(task_id)
    except:
        task_id = "DSP/" + re.findall("task_id\.(\d*)", notebook_filename)[0]
        results[task_id].append(False)


total, correct = [], []
for result in results.values():
    result.sort()
    passed = [bool(r) for r in result]
    total.append(len(passed))
    correct.append(sum(passed))
total = np.array(total)
correct = np.array(correct)
print("Tests array")
print(total)
print("Correct array")
print(correct)

# ks = [1, 10, 100]
ks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
pass_at_k = {f"pass@{k}": estimate_pass_at_k(total, correct, k).mean() \
                                                for k in ks if (total >= k).all()}
print(pass_at_k)

print(f"# Tests {np.sum(total)}")
print(f"# Correct {np.sum(correct)}")

# with open("samples.jsonl", "r") as f_samples:
#     problems = f_samples.readlines()

# for line in problems:
#     problem = json.loads(line)
#     print(problem["task_id"])
#     # print(problem["completion"] + "\n" + problem["test"])

#     try:
#         exec(problem["completion"] + "\n" + problem["test"])
#         passed = True
#     except Exception as e:
#         passed = False
#         print(e)

#     print("Outcome:", passed)

