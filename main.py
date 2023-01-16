import requests
from bs4 import BeautifulSoup
import json
import csv

# Делаем запрос на сайт и скачиваем исходный код страницы в index.html
url = 'https://sevastopol.kinoafisha.info/cinema/8321830/schedule/'

# Указываем аунтификацию
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agenr': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0 (Edition Yx 05)'
}

req = requests.get(url, headers=headers)
src = req.text

# Записываем исходный код страницы
with open('index.html', 'w', encoding='utf-8') as file:
    file.write(src)

# Открываем index.html, извлекаем необходимую информацию и записываем ее в json формат
with open('index.html', encoding="utf-8") as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

# Выбираем интерисующие нас данные(названия и ссылки на фильмы)
movie_names = soup.find_all(class_='showtimesMovie_name')
movie_link = soup.find_all(class_='showtimesMovie_link')

# Записываем в список назание фильмов
names = []
for name in movie_names:
    name_text = name.text
    names.append(name_text)

# Записываем в список ссылки на фильмы
links = []
for link in movie_link:
    link_href = link.get('href')
    links.append(link_href)

# Объединяем название и ссылки в словарь
names_links = dict(zip(names, links))

# Создаем json файл из словаря
with open('names_links.json', 'w') as file:
    json.dump(names_links, file, indent=4, ensure_ascii=False)

# Открывем файл json
with open('names_links.json') as file:
    all_movie = json.load(file)

# Создаем счетчики для итераций и их отслеживания
iteration_count = int(len(all_movie))
count = 0
print(f'Всего итераций: {iteration_count}')

# Заменяем пробелы в названиях на '_'
for all_name, all_link in all_movie.items():

    rep = [' ', '«', '»']
    for item in rep:
        if item in all_name:
            all_name = all_name.replace(item, '_')

    req = requests.get(url=all_link, headers=headers)
    src = req.text

    # Записываем исходный код страницы в директорию deepPars
    with open(f'deeppars/HTML/{count}{all_name}.html', 'w', encoding='utf-8') as file:
        file.write(src)

    # Считываем исходный код из файла
    with open(f'deeppars/HTML/{count}{all_name}.html', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # Собираем заголовки таблицы
    genre_tag = soup.find(class_='filmInfo_genreCell')
    description_tag = soup.find(class_='filmInfo_info swipe outer-mobile inner-mobile').find_all(class_='filmInfo_infoName')
    genre = genre_tag.text
    duration = description_tag[0].text
    release_yaer = description_tag[1].text
    premiere = description_tag[2].text
    age = description_tag[3].text

    # Записываем заголовки в файл csv
    with open(f'deeppars/CSV/{count}_{all_name}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                genre, duration, release_yaer, premiere, age
            )
        )
    # Собираем данные для заполнения таблицы
    genre_data = soup.find(class_='filmInfo_genreMenu menuBtn').find_all(class_='filmInfo_genreItem button-main')

    # Создаем списоки, в 1 будут записаны жанры, 2 превратив в json файл
    genre = []
    movie_info = []

    # Итерируемся и записываем жанры
    for item in genre_data:
        genre.append(item.text)

    # Находим и записываем описание фильма
    description_data = soup.find(class_='filmInfo_info swipe outer-mobile inner-mobile').find_all(class_='filmInfo_infoData')
    duration = description_data[0].text
    release_yaer = description_data[1].text
    premiere = description_data[2].text
    age = description_data[3].text

    # Создаем словарь для json
    movie_info.append(
        {
            'Genre': genre,
            'Duration': duration,
            'Release': release_yaer,
            'Premiere': premiere,
            'Age': age
        }
    )

    # Записываем данные в csv файл
    with open(f'deeppars/CSV/{count}_{all_name}.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                genre, duration, release_yaer, premiere, age
            )
        )

    # Создаем json файл со всеми фильмами
    with open(f'deeppars/JSON/{count}_{all_name}.json', 'a', encoding='utf-8') as file:
        json.dump(movie_info, file, indent=4, ensure_ascii=False)

    # Выводим счетчики для наглядности
    count += 1
    print(f'Итерция:{count}. {all_name}')
    iteration_count = iteration_count - 1
    print(f'Осталось итераций: {iteration_count}')