import csv

INPUT = 'questions/QuestionBank.csv'

# Fixes: {id: {field: new_value}}
# Focusing on:
# 1. Option D being a duplicate of the correct answer -> replace with a unique distractor
# 2. Plain math expressions in options -> wrap with \(...\)
FIXES = {
    '401': {
        # D duplicates C. Replace D with a real distractor.
        'optionD': 'Finite (non-zero) input impedance',
    },
    '402': {
        # D duplicates B (Zero). Replace with distractor.
        'optionD': 'Infinite',
    },
    '407': {
        # D duplicates A. Replace with distractor.
        'optionD': 'It oscillates indefinitely',
    },
    '408': {
        # D duplicates C. Replace with distractor.
        'optionD': 'Reduce input impedance to zero',
    },
    '409': {
        # D duplicates C. Replace with distractor.
        'optionD': 'Current-controlled voltage source',
    },
    '410': {
        # D duplicates C. Replace with distractor.
        'optionD': 'To maximize power dissipation in the op-amp',
    },
    '411': {
        # D duplicates B. Replace with distractor.
        'optionD': 'To convert capacitance to resistance',
    },
    '412': {
        # D duplicates B (Vi). Replace with distractor.
        'optionD': '2Vi',
    },
    '413': {
        # D duplicates A. Replace with distractor.
        'optionD': r'\(-1\,\text{V}\)',
    },
    '414': {
        # C and D both = -6. C should be different distractor.
        'optionC': '-4',
    },
    '415': {
        # C and D both = 12. C should be different.
        'optionC': '11',
    },
    '416': {
        # D duplicates A. Replace with distractor.
        'optionD': r'\(4\,\text{A}\)',
    },
    '417': {
        # D duplicates B. Replace with distractor. Also apply LaTeX to options.
        'optionA': r'\(\frac{V_1}{R_1} \cdot R_2\)',
        'optionB': r'\(-\frac{V_1}{R_1} \cdot R_2\)',
        'optionC': r'\(V_1\)',
        'optionD': r'\(\frac{R_2}{R_1 + R_2} \cdot V_1\)',
    },
    '418': {
        # D duplicates A. Apply LaTeX and unique D.
        'optionA': r'\(-\frac{V_1 \cdot R_2}{R_1 \cdot R_3}\)',
        'optionB': r'\(\frac{V_1 \cdot R_2}{R_1 \cdot R_3}\)',
        'optionC': r'\(\frac{V_2}{R_1}\)',
        'optionD': r'\(\frac{V_1}{R_3}\)',
    },
    '419': {
        # C and D are same. Replace D with unique distractor.
        'optionD': r'\(\left(\frac{R_2}{R_1}\right) V_{in}\)',
    },
    '420': {
        # Options A-C already have LaTeX. D = "Picture" which is wrong.
        'optionD': r'\(\left(-\frac{R_1}{R_2}\right) V_{in}\)',
    },
}

with open(INPUT, 'r', encoding='utf-8-sig', errors='replace', newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

changed = 0
for row in rows:
    qid = row.get('id', '').strip()
    if qid in FIXES:
        for field, val in FIXES[qid].items():
            row[field] = val
            changed += 1

with open(INPUT, 'w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Done. Applied {changed} field-level fixes to Topic 4.")
