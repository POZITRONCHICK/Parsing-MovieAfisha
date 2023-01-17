import requests
from bs4 import BeautifulSoup
import json

# Делаем запрос на сайт и скачиваем исходный код страницы в index.html
url = 'https://sevastopol.kinoafisha.info/movies/'

# Указываем аунтификацию
headers = {
    'accept': '*/*',
    'user-agenr': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0 (Edition Yx 05)'
}

req = requests.get(url, headers=headers)
src = req.text

# Записываем исходный код страницы
with open('indexmovie.html', 'w', encoding='utf-8') as file:
    file.write(src)

# Открываем index.html, извлекаем необходимую информацию и записываем ее в json формат
with open('indexmovie.html', encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

# Выбираем интерисующие нас данные(названия и ссылки на фильмы)
movie_names_links = soup.find_all(class_='movieItem_title')

# Создаем списки с названием и ссылками
names_list = []
links_list = []
for item in movie_names_links:
    names = item.text
    links = item.get('href')
    names_list.append(names)
    links_list.append(links)

# Объединяем название и ссылки в словарь
movie_general = dict(zip(names_list, links_list))

# Создаем json файл из словаря
with open('movie_general.json', 'w') as file:
    json.dump(movie_general, file, indent=4, ensure_ascii=False)

# Открывем файл json
with open('movie_general.json') as file:
    movie_general_json = json.load(file)

# Создаем счетчики для итераций и их отслеживания
iteration_count = int(len(movie_general_json))
count = 0
print(f'Всего итераций: {iteration_count}')

# Заменяем символы в названиях на '_'
for all_name, all_link in movie_general_json.items():
    rep = [' ', '«', '»', ':', '.', '-']
    for item in rep:
        if item in all_name:
            all_name = all_name.replace(item, '_')

    # Обращаемся к html страницы
    req = requests.get(url=all_link, headers=headers)
    src = req.text

    # Записываем исходный код страницы в директорию html_movie
    with open(f'html_movie/{count}{all_name}.html', 'w', encoding='utf-8') as file:
        file.write(src)

    # Считываем исходный код из файла
    with open(f'html_movie/{count}{all_name}.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # Считываем заголовок 'жанр'
    genre_tag = soup.find(class_='filmInfo_genreCell')
    genre = genre_tag.text

    # Считываем данные из жанра
    genre_data_tag = soup.find_all(class_='filmInfo_genreItem button-main')
    genre_list = []
    for item in genre_data_tag:
        genre_list.append(item.text)
    genre_data = ', '.join(genre_list)

    # Записываем заголовки и их наполнение
    head = soup.find(class_='filmInfo_info swipe outer-mobile inner-mobile').find_all(class_='filmInfo_infoName')
    description = soup.find(class_='filmInfo_info swipe outer-mobile inner-mobile').find_all(class_='filmInfo_infoData')

    head_list = [genre]
    for item in head:
        head_list.append(item.text)

    description_list = [genre_data]
    for item in description:
        description_list.append(item.text)

    # Создаем словарь из 2-х списков с заголовками и наполнением
    head_description = dict(zip(head_list, description_list))

    # Создаем json файл
    with open(f'json_movie/{count}_{all_name}.json', 'w', encoding='utf-8') as file:
        json.dump(head_description, file, indent=4, ensure_ascii=False)

    # Выводим счетчики для наглядности
    count += 1
    print(f'Итерция:{count}. {all_name}')
    iteration_count = iteration_count - 1
    print(f'Осталось итераций: {iteration_count}')