import csv
import urllib.request
import os

os.makedirs('tmp_images', exist_ok=True)
with open('questions/QuestionBank.csv', encoding='utf-8-sig', errors='replace') as f:
    for row in csv.DictReader(f):
        if row['topicId'] == '3' and row['image'].startswith('http'):
            fname = row['image'].split('/')[-1].split('?')[0]
            try:
                urllib.request.urlretrieve(row['image'], f'tmp_images/{fname}')
                print(f"Downloaded {fname}")
            except Exception as e:
                print(f"Failed to download {fname}: {e}")
