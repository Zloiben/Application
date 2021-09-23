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

# film = 'Test'
# rating = 0 - 10
# release = '00.00.0000'
# style = 'test'
