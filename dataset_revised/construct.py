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
files=[str(i) for i in range(1, 37)]

for file in files:
    file_path = os.path.join('./', file + '.txt')
    with open(file_path, 'r') as f:
        text = f.read()
    context = text.split('<End of Context>')[0] + '<End of Context>'
    steps = text.split('<End of Context>')[1]
    steps = steps.split('<End of Plan>')[0]
    steps = steps.strip()
    steps = steps.split('\n')
    next_line = 0
    while next_line < len(steps):
        current_context = context
        if next_line > 0:
            current_context += '\n\n'
            current_context += '\n'.join(steps[:next_line]) + '\n'
            current_context += '\n<End of Plan>'
        thought = steps[next_line] + '\n'
        next_line += 1
        implement = steps[next_line] + '\n'
        next_line += 1
        response = thought + implement
        assert 'Thought(' == thought[:8] and 'Implement(' == implement[:10] and ')' == implement[-2]
        statement = implement[10:-1]
        # assert statement is of format variavle=function(arg1=arg1,arg2=arg2,...)
        assert '=' in statement and '(' in statement.split('=')[1] and ')' == statement[-1]
        dataset.append({"messages": [{"role": "system", "content": sys_text}, {"role": "user", "content": current_context}, {"role": "assistant", "content": response}]})
        while next_line < len(steps) and '</result>' not in steps[next_line]:
            if 'Thought(' in steps[next_line]:
                raise Exception(f'{file}.txt: <result> is not closed')
            next_line += 1
        next_line += 1

# write the dataset into a json file
with open('dataset.jsonl', 'w') as f:
    for data in dataset:
        # Convert the dictionary to a JSON string with double quotes
        json_string = json.dumps(data)  # `json.dumps` ensures double quotes are used
        f.write(json_string + '\n')
