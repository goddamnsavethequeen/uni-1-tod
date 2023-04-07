import numpy as np

'1'

arr = np.genfromtxt('minutes_n_ingredients.csv', dtype='int32', delimiter=',', skip_header=1)
print(f'Первые 5 строк массива:\n{arr[:5]}')

'2'

arr_mean = np.mean(arr, axis=0)
print(f'Среднее значение первого столбца: {arr_mean[1]}, второго столбца: {arr_mean[2]}')

arr_min = np.amin(arr, axis=0)
print(f'Минимальное значение первого столбца: {arr_min[1]}, второго столбца: {arr_min[2]}')

arr_max = np.amax(arr, axis=0)
print(f'Максимальное значение первого столбца: {arr_max[1]}, второго столбца: {arr_max[2]}')

arr_median = np.median(arr, axis=0)
print(f'Медиана первого столбца: {arr_median[1]}, второго столбца: {arr_median[2]}')

'3'

arr_minutes = arr[:, 1]
arr_quantile = np.quantile(arr_minutes, 0.75, axis=0)
print(f'Ограниченный список минут: {arr_minutes[arr_minutes < arr_quantile]}')

'4'

arr_minutes = arr[:, 1]
print(f'Количество рецептов с продолжительностью 0: {len(arr_minutes[arr_minutes == 0])}')
# arr_minutes[arr_minutes == 0][:, 1] = 1

'5'

arr_id = arr[:, 0]
print(f'Количество уникальных рецептов: {len(np.unique(arr_id, axis=0))}')

'6'

arr_ingredients = arr[:, 2]
print(f'Количество различных значений количества ингредиентов: {len(np.unique(arr_ingredients, axis=0))}, их значения: {np.unique(arr_ingredients, axis=0)}')

'7'

arr_new = arr[arr[:, 2] <= 5]
print(f'Версия массива, где ингредиентов не более, чем 5:\n{arr_new}')

'8'

arr_null = arr[arr[:, 1] != 0][:, (1, 2)]
print(f'Максимальное значение величины "сколько в среднем ингредиентов приходится на одну минуту рецепта": {(arr_null[:, 1] / arr_null[:, 0]).max()}')

'9'

arr_sort = np.sort(arr[:, [0, 1, 2]], axis=0)[-100:-1, 2].mean()
print(f'Cреднее количество ингредиентов для топ-100 рецептов с наибольшей продолжительностью: {arr_sort}')

'10'

randoms = np.random.randint(len(arr), size=10)
print(f'10 случайно выбранных рецептов:\n{arr[randoms]}')

'11'

arr_mean_ingredient = np.mean(arr[:, 2], axis=0)
arr_mean_ingredients = arr[arr[:, 2] < arr_mean_ingredient]
print(f'Процент рецептов, количество ингредиентов в которых меньше среднего: {(len(arr_mean_ingredients) / len(arr)) * 100}')

'12'

mask_simple = (arr[:, 1] <= 20) & (arr[:, 2] <= 5)
arr_simple = np.insert(arr, 3, values=mask_simple, axis=1)
print(f'Версия массива с простыми рецептами:\n{arr_simple}')

'13'

arr_simple_pr = arr[mask_simple]
print(f'Процент простых рецептов: {(len(arr_simple_pr) / len(arr)) * 100}')
