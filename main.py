import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from config import *

# TODO: Улутшить интерфейс программы


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        #

        self.films = Films()
        self.serial = Serials()
        self.books_and_comics = BooksComics()

        #

        uic.loadUi('main.ui', self)

        #

        self.btn_films.clicked.connect(self.film_window)
        self.btn_serials.clicked.connect(self.serial_window)
        self.btn_books_and_comics.clicked.connect(self.books_and_comics_window)

    def film_window(self):
        self.films.show()
        ex.close()

    def serial_window(self):
        self.serial.show()
        ex.close()

    def books_and_comics_window(self):
        self.books_and_comics.show()
        ex.close()


class Films(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('film.ui', self)

        # TODO: Сделать сортировку по Критериям пользователя

        # -----------------------------------Базовый вывод фильмов------------------------------------------------------
        count = 1
        for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
            self.table_films.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'({value[2]}), '
                                             f'|{value[4]}|')
            count += 1

    # ----------------------------------------------Основные Критерии---------------------------------------------------
    # Кнопки Основных критерий
        self.btn_rating_DESC_films.clicked.connect(self.output_of_films_by_rating)
        self.btn_date_DESC_films.clicked.connect(self.output_of_films_by_date)
        self.btn_name_DESC_films.clicked.connect(self.output_of_films_by_name)

    #

    # №. film, [rating], (release), style, description
    # 1. Дюна, [8.1], (2021-09-09), Фантастика, Описание

    def output_of_films_by_rating(self):
        self.table_films.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
            self.table_films.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'({value[2]}), '
                                             f'|{value[4]}|')
            count += 1

    def output_of_films_by_date(self):
        self.table_films.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data ORDER BY release DESC"):
            self.table_films.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'({value[2]}), '
                                             f'|{value[4]}|')
            count += 1

    def output_of_films_by_name(self):
        self.table_films.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data ORDER BY film ASC"):
            self.table_films.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'({value[2]}), '
                                             f'|{value[4]}|')
            count += 1

    # ------------------------------------------------------------------------------------------------------------------


class Serials(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('serials.ui', self)

        # TODO: Добавить сортировку по критериям пользователя

    # ----------------------------------------------Основные Критерии---------------------------------------------------
        # Кнопки Основных критерий

        self.btn_date_DESC_serials.clicked.connect(self.output_of_serials_by_date)
        self.btn_name_DESC_serials.clicked.connect(self.output_of_serials_by_name)
        self.btn_rating_DESC_serials.clicked.connect(self.output_of_serials_by_rating)

        #

        # №. serial, [rating], (release), style, seasons, description
        #

        count = 1
        for value in sql.execute("SELECT * FROM data_serials ORDER BY release DESC"):
            self.table_serials.appendPlainText(f'{count}. '
                                               f'{value[0]}, '
                                               f'[{value[1]}], '
                                               f'{value[2]}, '
                                               f'({value[3]}), '
                                               f'|{value[4]}|')
            count += 1

    def output_of_serials_by_rating(self):
        self.table_serials.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data_serials ORDER BY rating DESC"):
            self.table_serials.appendPlainText(f'{count}. '
                                               f'{value[0]}, '
                                               f'[{value[1]}], '
                                               f'{value[2]}, '
                                               f'({value[3]}), '
                                               f'|{value[4]}|')
            count += 1

    def output_of_serials_by_date(self):
        self.table_serials.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data_serials ORDER BY release DESC"):
            self.table_serials.appendPlainText(f'{count}. '
                                               f'{value[0]}, '
                                               f'[{value[1]}], '
                                               f'{value[2]}, '
                                               f'({value[3]}), '
                                               f'|{value[4]}|')
            count += 1

    def output_of_serials_by_name(self):
        self.table_serials.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data_serials ORDER BY serial ASC"):
            self.table_serials.appendPlainText(f'{count}. '
                                               f'{value[0]}, '
                                               f'[{value[1]}], '
                                               f'{value[2]}, '
                                               f'({value[3]}), '
                                               f'|{value[4]}|')
            count += 1

    # ------------------------------------------------------------------------------------------------------------------


class BooksComics(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('books_comics.ui', self)

    # TODO: Сделать сортировку по Критериям пользователя

    # ----------------------------------------------Основные Критерии---------------------------------------------------
        # Кнопки Основных критерий
        self.btn_date_DESC_books.clicked.connect(self.output_of_books_by_date)
        self.btn_name_DESC_books.clicked.connect(self.output_of_books_by_name)

        #

        # №. book_name, [release], author, (style), toms, description
        # 4. Восхождение Героя Щита. Том 11, [2021], Кю Айя, (Манга), 12, Описание

        count = 1
        for value in sql.execute("SELECT * FROM data_books ORDER BY release DESC"):
            self.table_books.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'{value[2]}, '
                                             f'({value[3]}), '
                                             f'|{value[4]}|')
            count += 1

    def output_of_books_by_date(self):
        self.table_books.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data_books ORDER BY release DESC"):
            self.table_books.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'{value[2]}, '
                                             f'({value[3]}), '
                                             f'|{value[4]}|')
            count += 1

    def output_of_books_by_name(self):
        self.table_books.clear()
        count = 1
        for value in sql.execute("SELECT * FROM data_books ORDER BY book_name ASC"):
            self.table_books.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'{value[2]}, '
                                             f'({value[3]}), '
                                             f'|{value[4]}|')
            count += 1

    # ------------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
