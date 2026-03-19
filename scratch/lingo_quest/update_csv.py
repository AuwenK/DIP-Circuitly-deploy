import csv

# Dictionary of resolved answers
updates = {
    '503': 'C',
    '504': 'A',
    '505': 'A',
    '401': 'C',
    '402': 'B',
    '419': 'C',
    '704': 'B',
    '705': 'A',
    '706': 'C',
    '707': 'C',
    '708': 'B',
    '709': 'A',
    '710': 'B',
    '711': 'B',
    '712': 'A',
    '713': 'B',
    '714': 'C',
    '715': 'B',
    '716': 'C',
    '717': 'C'
}

filename = 'questions/QuestionBank.csv'
temp_file = 'questions/QuestionBank_temp.csv'

with open(filename, 'r', encoding='utf-8-sig', errors='replace') as infile, open(temp_file, 'w', encoding='utf-8-sig', newline='') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    count = 0
    for row in reader:
        if row['id'] in updates and not row['answer'].strip():
            row['answer'] = updates[row['id']]
            count += 1
            print(f"Updated Q{row['id']} to Answer {row['answer']}")
        writer.writerow(row)
        
print(f"Total equations updated: {count}")
import os
os.replace(temp_file, filename)
print("Finished updating QuestionBank.csv.")
