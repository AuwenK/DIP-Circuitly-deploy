import csv
import urllib.request
import os

os.makedirs('tmp_images', exist_ok=True)
with open('questions/QuestionBank.csv', encoding='utf-8-sig', errors='replace') as f:
    for row in csv.DictReader(f):
        topic_id = row['topicId']
        if topic_id in ['4', '5', '6', '7', '8']:
            print(f"[{topic_id}] Q{row['id']}: {row['question']}")
            print(f"  A: {row['optionA']}")
            print(f"  B: {row['optionB']}")
            print(f"  C: {row['optionC']}")
            print(f"  D: {row['optionD']}")
            print(f"  Ans: {row['answer']}")
            print(f"  Image: {row['image']}")
            print()
            
            if row['image'].startswith('http'):
                fname = row['image'].split('/')[-1].split('?')[0]
                img_path = f'tmp_images/{fname}'
                if not os.path.exists(img_path):
                    try:
                        urllib.request.urlretrieve(row['image'], img_path)
                        print(f"  -> Downloaded {fname}")
                    except Exception as e:
                        print(f"  -> Failed to download {fname}: {e}")
