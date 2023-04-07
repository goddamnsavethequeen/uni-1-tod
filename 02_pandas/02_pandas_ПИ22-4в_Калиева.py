import pandas as pd

'1.1'

recipes = pd.read_csv('recipes_sample.csv', parse_dates=[4])
print(recipes, '\n')
reviews = pd.read_csv('reviews_sample.csv')
print(reviews, '\n')

'1.2'

print(f'1.2. Количество точек данных (строк) в recipes: {len(recipes)}, в reviews: {len(reviews)}')
print(f'1.2. Количество столбцов в recipes: {len(recipes.columns)}, в reviews: {len(reviews.columns)}')
print(f'1.2. Тип данных столбцов в recipes:\n{recipes.dtypes},\n\nв reviews:\n{reviews.dtypes}\n')

'1.3'

recipes_null = recipes.isnull()
reviews_null = reviews.isnull()
print(f'1.3. В каких столбцах таблиц содержатся пропуски в recipes:\n{recipes_null.sum()},\n\nв reviews:\n{reviews_null.sum()}\n')
print(f'1.3. Доля строк, содержащих пропуски, в отношении к общему количеству строк в recipes: {recipes_null.any(axis=1).sum() / len(recipes) * 100}, в reviews: {reviews_null.any(axis=1).sum() / len(reviews) * 100}')

'1.4'

print(f'1.4. Среднее значение для каждого из числовых столбцов в recipes: "minutes" - {recipes["minutes"].mean()}, в reviews: "rating" - {reviews["rating"].mean()}')

'1.5'

print(f'1.5. Серия из имен десяти случайных рецептов:\n{recipes.sample(n=10)["name"]}')

'1.6'

print('1.6. Сделано по умолчанию')

'1.7'

print(f'1.7. Информация о рецептах, время выполнения которых не больше 20 минут и кол-во ингредиентов в которых не больше 5: {len(recipes[(recipes["minutes"] <= 20) & (recipes["n_ingredients"] <= 5)])}')

'2.1'

print(f'2.1. Преобразованный столбец даты из таблицы recipes:\n{recipes["submitted"]}')

'2.2'

recipes_2010 = recipes[recipes['submitted'] < '2011-01-01']
print(f'2.2. Информация о рецептах, добавленных в датасет не позже 2010 года:\n{recipes_2010}')

'3.1'

recipes['description_length'] = recipes['description'].str.len().fillna(0).astype('int64')
print(f"3.1. Столбец description_length:\n{recipes['description_length']}")

'3.2'

recipes['name'] = recipes['name'].str.title()
print(f"3.2. Каждое слово в названии начинается с прописной буквы:\n{recipes['name']}")

'3.3'

recipes['name_word_count'] = recipes['name'].str.split().str.len()
print(f"3.3. Столбец, где хранится количество слов из названия рецепта:\n{recipes['name_word_count']}")

'6.1'

print(recipes.sort_values('name_word_count').to_csv('pandas_6-1.csv', encoding='utf-8', index=False))

'4.1'

print(f"4.1. Участник, который добавил максимальное количество рецептов: {recipes.groupby('contributor_id').count().sort_values('id', ascending=False).iloc[0].name}")

'4.2'

print(f"4.2. Средний рейтинг к каждому из рецептов:\n{reviews.groupby('recipe_id')['rating'].mean()}")
print(f"4.2. Отзывы с отсутствием рецептов: {len(recipes) - reviews['recipe_id'].nunique()}")

'4.3'

recipes['year'] = pd.DatetimeIndex(recipes['submitted']).year
recipes['year_count'] = 1
print(f"4.3. Количество рецептов с разбивкой по годам создания:\n{recipes.groupby('year')['year_count'].count()}")

'5.1'

recipes_reviews = (reviews.merge(recipes[['id', 'name', 'submitted']], left_on='recipe_id', right_on='id'))[['id', 'name', 'user_id', 'rating']]
print(f'5.1. Объединенная таблица:\n{recipes_reviews}')

'5.2'

recipes_reviews_new = (reviews.merge(recipes[['id', 'name', 'submitted']], left_on='recipe_id', right_on='id'))[['recipe_id', 'name']]
reviews['review_count'] = 0
recipes_reviews_new = (recipes_reviews_new.merge(reviews.groupby('recipe_id')['review_count'].count(), on='recipe_id'))
print(f'5.2. Объединенная таблица:\n{recipes_reviews_new}')

'5.3'

recipes_rating = reviews.merge(recipes[['id', 'name', 'submitted']], left_on='recipe_id', right_on='id')
recipes_rating['date'] = pd.to_datetime(recipes_rating['date'])
print(f"5.3. Pецепты, добавленные в каком году, имеют наименьший средний рейтинг:\n{recipes_rating[['date', 'rating']].groupby(recipes_rating['date'].dt.year)['rating'].mean().sort_values()}")

'6.2'

with pd.ExcelWriter('pandas_6-2.xlsx') as writer:
    recipes_reviews.to_excel(writer, sheet_name='Рецепты с оценками')
    recipes_reviews_new.to_excel(writer, sheet_name='Количество отзывов по рецептам')