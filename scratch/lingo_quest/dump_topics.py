import csv, sys

topic_id = sys.argv[1] if len(sys.argv) > 1 else '3'
filename = 'questions/QuestionBank.csv'

with open(filename, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        if row.get('topicId') == topic_id:
            count += 1
            print(f"Q{row['id']}: {row['question']}")
            print(f"  A: {row['optionA']}")
            print(f"  B: {row['optionB']}")
            print(f"  C: {row['optionC']}")
            print(f"  D: {row['optionD']}")
            print(f"  >>> Answer: {row['answer']}")
            print()
    print(f"--- Total: {count} questions for topic {topic_id} ---")
