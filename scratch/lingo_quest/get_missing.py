import csv

missing = ['401', '402', '413', '415', '419', 
           '503', '504', '505', '506', '507', '508', '509', '510', '511', '512',
           '704', '705', '706', '707', '708', '709', '710', '711', '712', '713', '714', '715', '716', '717']

with open('questions/QuestionBank.csv', encoding='utf-8-sig', errors='replace') as f:
    for row in csv.DictReader(f):
        if row['id'] in missing:
            print(f"Q{row['id']}: {row['question']}")
            print(f"  A: {row['optionA']}")
            print(f"  B: {row['optionB']}")
            print(f"  C: {row['optionC']}")
            print(f"  D: {row['optionD']}")
            print(f"  Ans: {row['answer']}")
            print(f"  Image: {row['image']}")
            print()
