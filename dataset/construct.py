import os
import json

# read all files in the directory
def read_files(directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith(".txt"):
            filename = file.split(".")[0]
            if filename != 'sys':
                files.append(filename)
    return files

# read the system file and store the text into a string. Turn '"' to be '\"'.
def read_sys_file(directory):
    sys_file = 'sys.txt'
    sys_file_path = os.path.join(directory, sys_file)
    with open(sys_file_path, 'r') as f:
        sys_text = f.read()
    return sys_text

def longest_common_prefix(s1, s2):
    i = 0
    while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
        i += 1
    return s1[:i]

sys_text = read_sys_file('./')

dataset = []
files = read_files('./')
# files=['7']

for file in files:
    file_path = os.path.join('./', file + '.txt')
    with open(file_path, 'r') as f:
        text = f.read()
    context = text.split('<End of Context>')[0] + '<End of Context>'
    thought = text.split('<End of Context>')[1].split('<End of Thought>')[0] + '<End of Thought>'
    plan = text.split('<End of Thought>')[1].split('<End of Plan>')[0] + '<End of Plan>'
    modified_plans = []
    _text = text.split('<End of Plan>')[1]
    while '<End of Modified Plan>' in _text:
        modified_plans.append(_text.split('<End of Modified Plan>')[0] + '<End of Modified Plan>')
        _text = '<End of Modified Plan>'.join(_text.split('<End of Modified Plan>')[1:])
    dataset.append({"messages": [{"role": "system", "content": sys_text}, {"role": "user", "content": context}, {"role": "assistant", "content": thought}]})
    dataset.append({"messages": [{"role": "system", "content": sys_text}, {"role": "user", "content": context + thought}, {"role": "assistant", "content": plan}]})
    for i, modified_plan in enumerate(modified_plans):
        previous_plan = plan
        if i > 0:
            previous_plan = modified_plans[i - 1]
        # get lcs between previous plan and modified plan
        lcs = longest_common_prefix(previous_plan, modified_plan)
        # check if the modified plan after lcs starts with Implement(...) and <result></result>. If yes, insert <result>...</result> into the plan after lcs.
        if '<result>' in modified_plan[len(lcs):]:
            result = modified_plan[len(lcs):].split('<result>')[1].split('</result>')[0]
            previous_plan = lcs + '<result>' + result + '</result>\n' + lcs.join(previous_plan.split(lcs)[1:])
        previous_plan = previous_plan.replace('<End of Modified Plan>', '<End of Plan>')
        dataset.append({"messages": [{"role": "system", "content": sys_text}, {"role": "user", "content": context + thought + previous_plan}, {"role": "assistant", "content": modified_plan}]})

# write the dataset into a json file
with open('dataset.jsonl', 'w') as f:
    for data in dataset:
        # Convert the dictionary to a JSON string with double quotes
        json_string = json.dumps(data)  # `json.dumps` ensures double quotes are used
        f.write(json_string + '\n')
