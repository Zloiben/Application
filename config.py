import sqlite3

db = sqlite3.connect("database.db")
sql = db.cursor()

#

sql.execute("""CREATE TABLE IF NOT EXISTS data (
    film TEXT,
    rating REAL,
    release DATE,
    style TEXT, 
    description TEXT
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

sql.execute("""CREATE TABLE IF NOT EXISTS data_serials (
    serial TEXT,
    rating REAL,
    release DATE,
    style TEXT,
    seasons INT,
    description TEXT
)""")
db.commit()


# TODO: Увеличить базу данных

# ---------------------------------Данные возращаемы с базы данных Сериалов---------------------------------------------
# serial = 'Test'
# rating = 0 - 10
# release = 'YYYY-MM-DD'
# style = 'Test'
# seasons = 0 - n
# description = 'Test' -> Описание
# ---------------------------------Данные возращаемы с базы данных Книг-------------------------------------------------
# book_name = 'Test'
# release = 'YYYY'
# author = 'Test'
# style = 'Test'
# toms = 0 - n , Количесвто томов или частей у книги
# ---------------------------------Данные возращаемы с базы данных Фильмов----------------------------------------------
# film = 'Test'
# rating = 0 - 10
# release = 'YYYY-MM-DD'
# style = 'test'
# description = 'Test' -> Описание
# ----------------------------------------------------------------------------------------------------------------------

# Типы сортировки
# ASC - От меньшего к большему
# DESC - От большего к меньшему
#
# SELECT * FROM ... - Вывод информации с базы данных
