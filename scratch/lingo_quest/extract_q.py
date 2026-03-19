import csv
import sys

with open('questions/QuestionBank.csv', encoding='utf-8-sig', errors='replace') as f:
    for row in csv.DictReader(f):
        if row['topicId'] == '2':
            print(f"Q{row['id']}: {row['question']}")
            print(f"  A: {row['optionA']}")
            print(f"  B: {row['optionB']}")
            print(f"  C: {row['optionC']}")
            print(f"  D: {row['optionD']}")
            print(f"  Ans: {row['answer']}")
            print(f"  Image: {row['image']}")
            print()
