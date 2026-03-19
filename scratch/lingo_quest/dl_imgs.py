
import csv, urllib.request, os
os.makedirs('tmp_images', exist_ok=True)
with open('questions/QuestionBank.csv', encoding='utf-8') as f:
    for row in csv.DictReader(f):
        if row['topicId'] == '1' and row['image'].startswith('http'):
            fname = row['image'].split('/')[-1].split('?')[0]
            urllib.request.urlretrieve(row['image'], f'tmp_images/{fname}')
            print('Downloaded ' + fname + ' for Q' + str(row['id']))

