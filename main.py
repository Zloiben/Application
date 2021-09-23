import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from config import *


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

        #

        # TODO: Сделать сортировку по рейдину и по критериям пользователя
        count = 1
        for value in sql.execute("SELECT * FROM data"):
            # Вывод информации из базы данных database.db
            # 1. Шан-Чи и легенда десяти колец, 7.3, 2021, Фантастика
            self.table.appendPlainText(f'{count}. {value[0]}, {value[1]}, {value[2]}, {value[3]}')
            count += 1


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
