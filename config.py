import sqlite3

db = sqlite3.connect("database.db")
sql = db.cursor()

#

sql.execute("""CREATE TABLE IF NOT EXISTS data (
    film TEXT,
    rating REAL,
    release DATE,
    style TEXT
)""")
db.commit()

#

sql.execute("""CREATE TABLE IF NOT EXISTS data_books (
    book_name TEXT,
    release DATE,
    author TEXT,
    style TEXT,
    toms INT
)""")
db.commit()

#

sql.execute("""CREATE TABLE IF NOT EXISTS data_books (
    book_name TEXT,
    release DATE,
    author TEXT,
    style TEXT,
    toms INT
)""")
db.commit()


# TODO: Увеличить базу данных
# TODO: Добавить к переменной style еще несколько переменных для более точного поиска фильмов
# TODO: Изменить возращаемые данные у переменой release, кроме release у Книг
# '0000' -> '0000.00.00'
# ---------------------------------Данные возращаемы с базы данных Сериалов---------------------------------------------
# book_name = 'Test'
# release = '0000'
# style = 'Test'
# seasons = 0 - n
# ---------------------------------Данные возращаемы с базы данных Книг-------------------------------------------------
# book_name = 'Test'
# release = '0000'
# author = 'Test'
# style = 'Test'
# toms = 0 - n , Количесвто томов или частей у книги
# ---------------------------------Данные возращаемы с базы данных Фильмов----------------------------------------------
# film = 'Test'
# rating = 0 - 10
# release = '0000'
# style = 'test'
# ----------------------------------------------------------------------------------------------------------------------

# Типы сортировки
# ASC - От меньшего к большему
# DESC - От большего к меньшему
#
# SELECT * FROM data - Вывод информации с базы данных
