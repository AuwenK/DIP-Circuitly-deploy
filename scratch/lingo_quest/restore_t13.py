import csv
import shutil

INPUT = 'questions/QuestionBank.csv'
BACKUP = 'questions/QuestionBank_pre_revert_t13.csv'
FIXED_FILE = 'questions/QuestionBank_restored_t13.csv'

# 1. Load explanations from backup
backup_explanations = {}
with open(BACKUP, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('id') and row.get('topicId') in ('1', '2', '3') and row.get('explanation'):
            backup_explanations[row['id']] = row['explanation']

# 2. Add explanations to current data
rows = []
with open(INPUT, 'r', encoding='utf-8-sig', errors='replace', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        qid = row['id']
        if qid in backup_explanations:
            row['explanation'] = backup_explanations[qid]
        rows.append(row)

# 3. Write back the restored version
with open(FIXED_FILE, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# 4. Overwrite original
shutil.copy(FIXED_FILE, INPUT)

print(f"Restored Topic 1-3 explanations for {len(backup_explanations)} questions.")
