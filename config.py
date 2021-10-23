import sqlite3

db = sqlite3.connect("database.db")
sql = db.cursor()

# Таблица data - Фильмы
# id TEXT 1000001 (id нужно для простого сохранение фотографий)
# film TEXT Шан-Чи и легенда десяти колец
# rating REAL 9.1
# nation TEXT США
# release DATE 2021-05-09
# style TEXT Фантастика
# age TEXT 16+ (TODO: Изменить на число и выводить потом со знаком + для того что бы было использованно меньше памяти)
# description TEXT Описание
# images TEXT (images хранит ссылку для скачивание изображение с интерета используется библиотка urllib.request)

# Таблица data_books - Книги
# TODO: Нужно переделать под новые функции

# Таблица data_serials - СЕриалы
# TODO: Нужно переделать под новые функции


