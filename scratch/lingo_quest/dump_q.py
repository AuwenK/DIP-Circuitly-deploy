import csv

with open('questions/QuestionBank.csv', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['topicId'] in ['1', '2']:
            print(f"Q{row['id']}: {row['question']}")
            print(f"Ans: {row['answer']}")
            print()
