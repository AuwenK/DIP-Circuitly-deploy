import csv

with open('questions/QuestionBank.csv', encoding='utf-8-sig', errors='replace') as f:
    rows = [r for r in csv.DictReader(f) if r['topicId'] in ('1', '2')]

print(f"Total T1+T2 questions: {len(rows)}")
filled = [r for r in rows if r.get('explanation', '').strip()]
empty = [r for r in rows if not r.get('explanation', '').strip()]
print(f"With explanations: {len(filled)}")
print(f"Without explanations: {len(empty)}")

if empty:
    print("\nQuestions missing explanations:")
    for r in empty:
        print(f"  Q{r['id']} (Topic {r['topicId']}): {r['question'][:60]}")

if filled:
    print("\nSample explanation (Q101):")
    for r in filled[:1]:
        print(f"  {r['explanation'][:200]}")
