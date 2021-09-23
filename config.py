import sqlite3

db = sqlite3.connect("database.db")
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS data (
    film TEXT,
    rating REAL,
    release TEXT,
    style TEXT
)""")

db.commit()

# Данные возращаемы с базы данных
# film = 'Test'
# rating = 0 - 10
# release = '0000'
# style = 'test'

# Типы сортировки
# ASC - От меньшего к большему
# DESC - От большего к меньшему

# SELECT * FROM data - Вывод информации с базы данных
