import csv
import shutil

INPUT = 'questions/QuestionBank.csv'
shutil.copy(INPUT, 'questions/QuestionBank_backup_t4.csv')

FIXES = {
    '401': 'C',  # Infinite output impedance is NOT an ideal op-amp property (it should be ZERO)
    '402': 'B',  # Virtual short: difference = 0
    '404': 'A',  # Non-inverting amplifier gives positive gain
    '405': 'D',  # Non-inverting amplifier (image shows non-inverting config)
    '406': 'C',  # Resistor sets the gain (not diode)
    '407': 'A',  # Without feedback -> acts as comparator
    '408': 'C',  # Negative feedback -> stabilize and control closed-loop gain
    '409': 'C',  # Op-amp is a VCVS (Voltage-Controlled Voltage Source)
    '410': 'C',  # Zero output impedance -> output unaffected by load
    '411': 'B',  # Valid application: amplify voltage signals
    '412': 'B',  # Voltage follower: Vout = Vi
    '413': 'A',  # If Vi=0, Vout=0
    '414': 'D',  # Image-based: -6
    '415': 'D',  # Image-based: 12
    '416': 'A',  # Image-based: 1A
    '417': 'B',  # Inverting: VA = (-V1/R1)*R2
    '418': 'A',  # Current through R3 = (-V1/R1)*R2/R3
    '419': 'C',  # Non-inverting: (1+R2/R1)*Vin
    '420': 'A',  # Inverting: (-R2/R1)*Vin
}

with open(INPUT, 'r', encoding='utf-8-sig', errors='replace', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changed = []
for row in rows:
    if row['topicId'] == '4' and row['id'] in FIXES:
        old = row['answer']
        new = FIXES[row['id']]
        if old.strip() != new:
            changed.append(f"  Q{row['id']}: '{old.strip()}' -> '{new}'")
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
