import pandas as pd
import unittest
import csv
import json
import matplotlib.pyplot as plt
from typing import List, Any, Dict, Optional

recipes_100 = pd.read_csv('recipes_100.csv')
recipes_100

def time_mins(time_string: list) -> int:
  '''Принимает строку-время и возвращает соответствующее число минут'''
  all_time = []
  all_time = time_string.split()
  hrs, mins = 0, 0
  for i in range(len(all_time)):
    if all_time[i] == 'hrs': 
      hrs = int(all_time[i-1]) 
    if all_time[i] == 'mins': 
      mins = int(all_time[i-1])
  return (hrs*60 + mins)

class TestTimes(unittest.TestCase):
  def test_time1(self):
    self.assertEqual(time_mins('0 hrs 5 mins'), 5)
  def test_time2(self):
    self.assertEqual(time_mins('1 hrs'), 60)
  def test_time3(self):
    self.assertEqual(time_mins('0 hrs 0 mins'), 0)
  def test_time4(self):
    self.assertEqual(time_mins('2 hrs 0 mins'), 120)

unittest.main(argv = [''], verbosity=2, exit=False)

#Поиск рецептов, для приготовления которых используется определенный ингредиент (например, курица)
def rec_and_ingr(df: Any) -> List[str]:
  '''Функция принимает датафрейм, анализирует столбец ingredients на содержание вводимого ингредиента, возвращает названия блюд, в которых используется ингредиент введенный пользователем'''
  recipes_with_ingredients = {}
  count = 0
  for row in df: 
    if count > 0:
      recipes_with_ingredients[row[1]] = row[4]
    count += 1
  all_recipes = list(recipes_with_ingredients.keys())
  all_ingredients = list(recipes_with_ingredients.values())
  my_recipes = list()
  ingr = input()
  for i in range(len(all_ingredients)):
    if ingr in all_ingredients[i]:
      my_recipes.append(all_recipes[i])
  return my_recipes

with open("recipes_100.csv") as f:
    recipes = csv.reader(f)
    new_recipes: List[str] = rec_and_ingr(recipes)

#Поиск трех самых долгих по приготовлению рецептов
all_recipes = recipes100[['recipe_name', 'total_time']]
sorted_recipes = all_recipes.drop_duplicates()
times_recipes = sorted_recipes['total_time'].astype(str).apply(time_mins)
new_sorteds = times_recipes.sort_values(ascending=False)
index = new_sorteds[:3].index
dishes = sorted_recipes.loc[index, 'recipe_name']

#Определение блюд на каждое количество человек
def serving_recipes(df: Any) -> Dict[Optional[int], str]:
  '''Функция принимает датафрейм и выдает словарь, содержащий количество персон и названия блюд, которые на такое количество человек можно приготовить'''
  all_recipes = df[['recipe_name', 'servings']]
  sorted_recipes = all_recipes.drop_duplicates()
  servings_and_recipes = {}
  for i in range(len(df['servings'])):
    recipes = df[(df.servings == i)]['recipe_name']
    if recipes.empty == False:
      servings_and_recipes[i] = [*set(recipes)]
  return servings_and_recipes

servings: Dict[Optional[int], str] = serving_recipes(recipes_100)

#Создание .json файла с ответами
recipes_100_answeres = {
    'Recipes that contain chicken:': new_recipes,
    'The three longest of time recipes to make: ': list(dishes),
    'Names of dishes that can be prepared for each number of people:': servings
}
with open('answeres.json', 'w') as f:
  json.dump(recipes_100_answeres, f, indent=' ')


#Построение гистограммы на основе рейтинга блюд
rating = recipes_100.sort_values(by = 'rating')
new_rating = rating['rating']
plt.hist(new_rating, alpha = 0.5, color = 'purple', edgecolor = 'blue', bins = 15)
plt.grid(b=True, axis='y', color = 'black')
plt.title('Оценки блюд')
plt.xlabel('Рейтинг', size=15)
plt.ylabel('Количество блюд', size=15)
plt.savefig('hist.png')
