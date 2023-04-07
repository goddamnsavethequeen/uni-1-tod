import json as js
import pandas as pd
import pickle
from bs4 import BeautifulSoup
import numpy as np

'1.1'

contributors_sample = open('contributors_sample.json')
contributors_sample = js.load(contributors_sample)
print('1.1. Информацию о первых 3 пользователях:')
for i in range(3):
    print(contributors_sample[i], end='\n')

'1.2'

domains = []
for i in contributors_sample:
    domains.append(i['mail'].split('@')[1])
print(f'1.2. Уникальные почтовые домены: {set(domains)}')

'1.3'

def find_user(username):
    for user in contributors_sample:
        if user['username'] == username:
            print(user)
            break
    else:
        raise AttributeError
username = input('1.3. Введите username: ')
# username = 'sheilaadams'
print('1.3. Результат поиска человека по введенному username: ')
find_user(username)

'1.4'

count_female = 0
count_male = 0
for user in contributors_sample:
    if user['sex'] == 'F':
        count_female += 1
    elif user['sex'] == 'M':
        count_male += 1
print(f'1.4. Количество женщин в файле: {count_female}, мужчин: {count_male}')

'1.5'

contributors = pd.DataFrame({'id': [], 'username': [], 'sex': []})
for user in contributors_sample:
    contributors.loc[len(contributors)] = [user['id'], user['username'], user['sex']]
print(f'1.5. DataFrame "contributors":\n{contributors}')

'1.6'

recipes = pd.read_csv('recipes_sample.csv')
recipes_contributors = recipes.merge(contributors, left_on='contributor_id', right_on='id', how='left')
recipes_contributors = recipes_contributors[recipes_contributors['id_y'].isnull()]
recipes_contributors = recipes_contributors.reset_index()
print(f"1.6. Количество человек, для которых информация отсутствует: {len(recipes_contributors['contributor_id'].unique())}, объединенная таюлица:\n{recipes_contributors}")

'2.1'

jobs = []
job_people = dict()
for user in contributors_sample:
    jobs.append(user['jobs'])
jobs = set([a for job in jobs for a in job])
for user in contributors_sample:
    for job_user in user['jobs']:
        for job in jobs:
            if job_user == job:
                if job not in job_people:
                    job_people[job] = [user['username']]
                else:
                    job_people[job].append(user['username'])
print(f"2.1. Значения из созданного словаря:\n{job_people}")

'2.2'

job_people_pickle = open('job_people.pickle', 'wb')
pickle.dump(job_people, job_people_pickle)
job_people_pickle.close()

with open('job_people.json', 'w') as job_people_json:
    js.dump(job_people, job_people_json, indent=2)

'2.3'

file_pickle = open('job_people.pickle', 'rb')
data_pickle = pickle.load(file_pickle)
file_pickle.close()
print(f"2.3. Данные из файла job_people.pickle: {data_pickle}")

'3.1'

with open('steps_sample.xml', 'r') as f:
    file = f.read()
steps_sample = dict()
soup_steps_sample = BeautifulSoup(file, 'xml')
for recipe in soup_steps_sample.find_all('recipe'):
    steps_sample[recipe.find('id').text.strip()] = []
    for step in recipe.find_all('step'):
        steps_sample[recipe.find('id').text.strip()].append(step.text.strip())
with open('steps_sample.json', 'w') as steps_sample_json:
    js.dump(steps_sample, steps_sample_json, indent=2)

'3.2'

steps_sample_length = dict()
for id in steps_sample:
    if len(steps_sample[id]) not in steps_sample_length:
        steps_sample_length[len(steps_sample[id])] = [id]
    else:
        steps_sample_length[len(steps_sample[id])].append(id)
print(f'3.2. Словарь с количеством шагов в рецепте и список рецептов:\n{steps_sample_length}')

'3.3'

recipes_has_minutes = []
for recipe in soup_steps_sample.find_all('recipe'):
    for step in recipe.find_all('step'):
        if step.has_attr('has_minutes'):
            recipes_has_minutes.append(recipe.find('id').text.strip())
            break
print(f'3.3. Cписок рецептов, в этапах выполнения которых есть информация о времени: {recipes_has_minutes}')

'3.4'

recipes = pd.read_csv('recipes_sample.csv')
recipes['id'] = recipes['id'].astype('str')
for index, row in recipes.iterrows():
    if pd.isna(row['n_steps']):
        if row['id'] in steps_sample:
            recipes.at[index, 'n_steps'] = len(steps_sample[row['id']])
print(f'3.4. Таблица recipes с заполненным n_steps:\n{recipes}')

'3.5'

print(f"3.5. Проверяем, содержит ли столбец n_steps пропуски:\n{recipes['n_steps'].isnull().value_counts()}")
recipes['n_steps'] = recipes['n_steps'].astype('int64')
recipes.to_csv('recipes_sample_with_filled_nsteps.csv')
