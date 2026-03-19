import csv

with open('questions/QuestionBank.csv', encoding='utf-8-sig', errors='replace') as f:
    rows = [r for r in csv.DictReader(f) if r['topicId'] == '4']

for row in rows:
    print(f"=== Q{row['id']} ===")
    print(f"Q: {row['question']}")
    print(f"A: {row['optionA']}")
    print(f"B: {row['optionB']}")
    print(f"C: {row['optionC']}")
    print(f"D: {row['optionD']}")
    print(f"ANS: {row['answer']}")
    print()
