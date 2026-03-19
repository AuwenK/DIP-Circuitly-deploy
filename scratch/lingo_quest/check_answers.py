import re

with open('remaining_questions.txt', encoding='utf-16le') as f:
    lines = f.readlines()

current_q = None
missing_ans = []
for line in lines:
    if line.startswith('['):
        current_q = line.strip()
    elif line.strip().startswith('Ans:'):
        ans = line.strip().split('Ans:')[-1].strip()
        if not ans:
            missing_ans.append(current_q)

if missing_ans:
    print("Questions with missing answers:")
    for q in missing_ans:
        print(q)
else:
    print("All questions have answers assigned.")
