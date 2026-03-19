import csv

filename = 'questions/QuestionBank.csv'
with open(filename, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['topicId'] == '3':
            print(f"Q{row['id']}: {row['question']}")
            print(f"A: {row['optionA']}")
            print(f"B: {row['optionB']}")
            print(f"C: {row['optionC']}")
            print(f"D: {row['optionD']}")
            print(f"Ans: {row['answer']}")
            print("-" * 40)
