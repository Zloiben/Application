import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from config import *

# TODO: Увеличить базу данных
# TODO: Улутшить интерфейс программы


class Main(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        #

        self.btn_films.clicked.connect(self.film_window)
        self.btn_serials.clicked.connect(self.serial_window)
        self.btn_books_and_comics.clicked.connect(self.books_and_comics_window)

    def film_window(self):
        self.films = Films()
        self.films.show()

    def serial_window(self):
        self.serial = Serials()
        self.serial.show()

    def books_and_comics_window(self):
        self.books_and_comics = BooksComics()
        self.books_and_comics.show()


class Films(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('film.ui', self)

        # TODO: Сделать сортировку по Критериям пользователя

        # -----------------------------------Базовый вывод фильмов------------------------------------------------------
        count = 1
        for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
            # Вывод информации из базы данных database.db
            # 1. Шан-Чи и легенда десяти колец, 7.3, 2021, Фантастика
            self.table.appendPlainText(f'{count}. {value[0]}, {value[1]}, {value[2]}, {value[3]}')
            count += 1

    # ----------------------------------------------Основные Критерии---------------------------------------------------
    # Кнопки Основных критерий
        self.btn_rating_DESC.clicked.connect(self.output_of_films_by_rating)
        self.btn_date_DESC.clicked.connect(self.output_of_films_by_date)
        self.btn_name_DESC.clicked.connect(self.output_of_films_by_name)

    def output_of_films_by_rating(self):
        self.table.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
            # Вывод информации из базы данных database.db
            # 1. Шан-Чи и легенда десяти колец, 7.3, 2021, Фантастика
            self.table.appendPlainText(f'{count}. {value[0]}, {value[1]}, {value[2]}, {value[3]}')
            count += 1

    def output_of_films_by_date(self):
        self.table.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data ORDER BY release DESC"):
            # Вывод информации из базы данных database.db
            # 1. Шан-Чи и легенда десяти колец, 7.3, 2021, Фантастика
            self.table.appendPlainText(f'{count}. {value[0]}, {value[1]}, {value[2]}, {value[3]}')
            count += 1

    def output_of_films_by_name(self):
        self.table.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data ORDER BY film ASC"):
            # Вывод информации из базы данных database.db
            # 1. Шан-Чи и легенда десяти колец, 7.3, 2021, Фантастика
            self.table.appendPlainText(f'{count}. {value[0]}, {value[1]}, {value[2]}, {value[3]}')
            count += 1

    # ------------------------------------------------------------------------------------------------------------------


class Serials(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('serials.ui', self)
        

class BooksComics(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('books_comics.ui', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
