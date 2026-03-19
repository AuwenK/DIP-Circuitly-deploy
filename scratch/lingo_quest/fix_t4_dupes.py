import csv

INPUT = 'questions/QuestionBank.csv'

EXTRA = {
    # Q403: C and D both = "Inverting amplifier" -> give D a unique distractor
    '403': {'optionD': 'Voltage follower'},
    # Q406: C and D both = "Resistor" -> give D a unique distractor
    '406': {'optionD': 'Inductor'},
    # Q404: A and D both = "Non-inverting amplifier"
    '404': {'optionD': 'Summing amplifier'},
}

with open(INPUT, 'r', encoding='utf-8-sig', errors='replace', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

count = 0
for row in rows:
    qid = row.get('id', '').strip()
    if qid in EXTRA:
        for field, val in EXTRA[qid].items():
            row[field] = val
            count += 1

with open(INPUT, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done. Fixed {count} remaining duplicate options.")
