import json
from pathlib import Path
import nbformat
from nbclient import NotebookClient
from collections import defaultdict
import numpy as np
from tqdm import tqdm
from data_science_problems.utils import stream_jsonl, estimate_pass_at_k, reliability_guard

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
                # print(task_id, has_no_error(test))
                return has_no_error(test), task_id
            

def has_no_error(x):
    for element in x:
        if "ename" in element:
            return False
    return True


out_file = "generated.txt"

with open(out_file) as f:
    ps = f.readlines()

for line in ps:
    # notebook_filename = "juice-github-repos\mwizasimbeye11.data-science-africa-2018-abuja\data-science-africa-2018-abuja-master\PythonBasicsx.task_id.0.0.ipynb"
    notebook_filename = Path(line.strip())
    # print(notebook_filename)
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
    enb = client.execute()
    # print(notebook_filename)
    nbformat.write(enb, notebook_filename)
    # print(notebook_filename)

print("Complute pass@k for the executed notebooks.")
with open(out_file) as f:
    ps = f.readlines()

results = defaultdict(list)
for notebook_filename in tqdm(ps):
    result, task_id = evaluate(notebook_filename)
    results[task_id].append(result)

total, correct = [], []
for result in results.values():
    result.sort()
    passed = [bool(r) for r in result]
    total.append(len(passed))
    correct.append(sum(passed))
total = np.array(total)
correct = np.array(correct)
print("# Tests")
print(total)
print("# Correct")
print(correct)

# ks = [1, 10, 100]
ks = [1]
pass_at_k = {f"pass@{k}": estimate_pass_at_k(total, correct, k).mean() \
                                                for k in ks if (total >= k).all()}
print(pass_at_k)

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

