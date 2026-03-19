import csv
import shutil

INPUT = 'questions/QuestionBank.csv'
BACKUP = 'questions/QuestionBank_pre_revert_t13.csv'

# 1. Backup the current state
shutil.copy(INPUT, BACKUP)

# 2. Read and modify
rows = []
with open(INPUT, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        # Clear explanations for Topics 1, 2, and 3
        if row['topicId'] in ('1', '2', '3'):
            row['explanation'] = ''
        rows.append(row)

# 3. Write back
with open(INPUT, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Cleared explanations for Topics 1, 2, and 3 in {INPUT}.")
