import csv
import shutil
import os

INPUT = 'questions/QuestionBank.csv'
BACKUP = 'questions/QuestionBank_backup_t4.csv'
FIXED_FILE = 'questions/QuestionBank_repaired.csv'

# Fixes for Topic 4 answers
T4_FIXES = {
    '401': 'C', '402': 'B', '404': 'A', '405': 'D', '406': 'C',
    '407': 'A', '408': 'C', '409': 'C', '410': 'C', '411': 'B',
    '412': 'B', '413': 'A', '414': 'D', '415': 'D', '416': 'A',
    '417': 'B', '418': 'B', # Sign flip for Q418: current FROM ground is +V1*R2/(R1*R3)
    '419': 'C', '420': 'A'
}

# LaTeX formatting for Topic 4 options (specifically for formulas)
T4_LATEX = {
    '417': {
        'optionA': r'\(\frac{V_1}{R_1} \cdot R_2\)',
        'optionB': r'\(-\frac{V_1}{R_1} \cdot R_2\)',
        'optionC': r'\(V_1\)',
        'optionD': r'\(\frac{R_2}{R_1 + R_2} \cdot V_1\)',
    },
    '418': {
        'optionA': r'\(-\frac{V_1 \cdot R_2}{R_1 \cdot R_3}\)',
        'optionB': r'\(\frac{V_1 \cdot R_2}{R_1 \cdot R_3}\)',
        'optionC': r'\(\frac{V_2}{R_1}\)',
        'optionD': r'\(\frac{V_1}{R_3}\)',
    },
    '419': {
        'optionD': r'\(\left(\frac{R_2}{R_1}\right) V_{in}\)',
    },
    '420': {
        'optionD': r'\(\left(-\frac{R_1}{R_2}\right) V_{in}\)',
    }
}

# 1. Load current explanations
current_explanations = {}
with open(INPUT, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row.get('id') and row.get('explanation'):
            current_explanations[row['id']] = row['explanation']

# 2. Load the base data from backup (this has 20 questions for T4 and Topic 5, 6, 7)
with open(BACKUP, 'r', encoding='utf-8-sig', errors='replace') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = [r for r in reader if r.get('id') and r.get('topicId')]

# 3. Apply fixes and restore explanations
for row in rows:
    qid = row['id']
    # Restore Explanation if we have one in current
    if qid in current_explanations:
        row['explanation'] = current_explanations[qid]
    
    # Apply Topic 4 Answer Fixes
    if row['topicId'] == '4' and qid in T4_FIXES:
        row['answer'] = T4_FIXES[qid]
    
    # Apply Topic 4 LaTeX Fixes
    if row['topicId'] == '4' and qid in T4_LATEX:
        for field, val in T4_LATEX[qid].items():
            row[field] = val

# 4. Write back the repaired version
with open(FIXED_FILE, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# 5. Overwrite the original (backup first)
shutil.copy(INPUT, 'questions/QuestionBank_corrupted_backup.csv')
shutil.copy(FIXED_FILE, INPUT)

print(f"Repaired QuestionBank.csv. Restored {len(rows)} valid questions.")
print(f"Current Row Count: {len(rows)} (excluding blank ones)")
