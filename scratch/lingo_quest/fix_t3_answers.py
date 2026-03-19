import csv
import io

INPUT = 'questions/QuestionBank.csv'

# Correct answers for Topic 3 questions (keyed by question id)
FIXES = {
    '301': 'B',  # RC time constant: 10k * 10u = 0.1s => B
    '302': 'C',  # Capacitor voltage continuity: vC(0+) = vC(0-) = 5V => C
    '307': 'C',  # Underdamped: R^2 < 4L/C => C
    '310': 'C',  # Transient negligible after 5 tau => C (was A=1 tau, wrong)
    '313': 'B',  # Z_C = 1/(j*omega*C) => B
    '314': 'C',  # Z_L = j*omega*L => C
    '316': 'C',  # Pure inductor averages zero real power => C
    '317': 'B',  # Power factor = cos(theta) => B
    '319': 'B',  # RC low-pass filter output across capacitor => B
    '320': 'C',  # Total response = transient + steady-state => C
}

with open(INPUT, 'r', encoding='utf-8-sig', errors='replace', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changed = []
for row in rows:
    if row['topicId'] == '3' and row['id'] in FIXES:
        old = row['answer']
        new = FIXES[row['id']]
        if old != new:
            changed.append(f"  Q{row['id']}: '{old}' -> '{new}'")
            row['answer'] = new

print("Fixed answers:")
for c in changed:
    print(c)
print(f"\nTotal changes: {len(changed)}")

with open(INPUT, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print("QuestionBank.csv updated successfully.")
