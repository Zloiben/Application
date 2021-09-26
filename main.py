import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from config import *

# TODO: Улутшить интерфейс программы


def film_window():
    films.show()
    ex.close()


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        #

        global serial, films, books_and_comics

        films = Films()
        serial = Serials()
        books_and_comics = BooksComics()

        #

        uic.loadUi('main.ui', self)

        #

        self.btn_films.clicked.connect(film_window)
        self.btn_serials.clicked.connect(self.serial_window)
        self.btn_books_and_comics.clicked.connect(self.books_and_comics_window)

        self.btn_exit_main.clicked.connect(self.exit)

    def serial_window(self):
        serial.show()
        ex.close()

    def books_and_comics_window(self):
        books_and_comics.show()
        ex.close()

    def exit(self):
        ex.close()


class Films(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('film.ui', self)

    # ---------------------------------------------<Критерии>-----------------------------------------------------------
        self.data_criteria = set()

        # Критерии

        self.checkBox.clicked.connect(self.films_sort)
        self.checkBox_2.clicked.connect(self.films_sort)
        self.checkBox_3.clicked.connect(self.films_sort)

        #

        self.btn_rating_DESC_films.clicked.connect(self.output_of_films_by_rating)
        self.btn_date_DESC_films.clicked.connect(self.output_of_films_by_date)
        self.btn_name_DESC_films.clicked.connect(self.output_of_films_by_name)

        self.btn_exit_films.clicked.connect(self.exit)
        #

        self.search_btn.clicked.connect(self.search_criteria)
    # ----------------------------------------------<Базовый вывод>-----------------------------------------------------
        count = 1
        self.table_films.appendPlainText('№. film, [rating], (release), style, |description|\n')
        for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
            self.table_films.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'({value[2]}), '
                                             f'{value[3]}, '
                                             f'\nОписание: {value[4]}\n')
            count += 1

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

    # №. film, [rating], (release), style, |description|
    # 1. Дюна, [8.1], (2021-09-09), Фантастика, Описание

    def output_of_films_by_rating(self):
        self.table_films.clear()
        self.table_films.appendPlainText('№. film, [rating], (release), style, |description|\n')
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                    SELECT * FROM data WHERE style in {self.sort()} ORDER BY rating DESC"""):
                self.table_films.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'({value[2]}), '
                                                 f'{value[3]}, '
                                                 f'\nОписание: |{value[4]}|\n')
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
                self.table_films.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'({value[2]}), '
                                                 f'{value[3]}, '
                                                 f'\nОписание: |{value[4]}|\n')
                count += 1

    def output_of_films_by_date(self):
        self.table_films.clear()
        self.table_films.appendPlainText('№. film, [rating], (release), style, |description|\n')
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                        SELECT * FROM data WHERE style in {self.sort()} ORDER BY release DESC"""):
                self.table_films.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'({value[2]}), '
                                                 f'{value[3]}, '
                                                 f'\nОписание: |{value[4]}|\n')
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY release DESC"):
                self.table_films.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'({value[2]}), '
                                                 f'{value[3]}, '
                                                 f'\nОписание: |{value[4]}|\n')
                count += 1

    def output_of_films_by_name(self):
        self.table_films.clear()
        self.table_films.appendPlainText('№. film, [rating], (release), style, |description|\n')
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                                    SELECT * FROM data WHERE style in {self.sort()} ORDER BY film ASC"""):
                self.table_films.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'({value[2]}), '
                                                 f'{value[3]}, '
                                                 f'\nОписание: |{value[4]}|\n')
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY film ASC"):
                self.table_films.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'({value[2]}), '
                                                 f'{value[3]}, '
                                                 f'\nОписание: |{value[4]}|\n')
                count += 1

    # --------------------------------------------Сортировка Критерий---------------------------------------------------

        # Входные данные: {'Фантастика', 'Ужасы'}
        # Возращает: ('Фантастика', 'Ужасы')
        # Нужно для команды в базу данных и для избежание не верных выводов данных
        # SELECT * FROM data WHERE style in ('Фантастика', 'Ужасы')

    def sort(self):
        return f'''('{"', '".join(self.data_criteria)}')'''

    def films_sort(self, state):
        if state:
            self.data_criteria.add(self.sender().text())
        else:
            self.data_criteria.remove(self.sender().text())

    def search_criteria(self):
        self.table_films.clear()
        self.table_films.appendPlainText('№. film, [rating], (release), style, |description|\n')
        count = 1
        for value in sql.execute(f"SELECT * FROM data WHERE style in {self.sort()} ORDER BY rating DESC"):
            self.table_films.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'({value[2]}), '
                                             f'{value[3]}, '
                                             f'\nОписание: |{value[4]}|\n')
            count += 1

    #  -----------------------------------------------------------------------------------------------------------------

    def exit(self):
        films.close()
        ex.show()


class Serials(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('serials.ui', self)

        self.data_criteria_serials = set()

        # Критерии

        self.checkBox.clicked.connect(self.serials_sort)
        self.checkBox_2.clicked.connect(self.serials_sort)
        self.checkBox_3.clicked.connect(self.serials_sort)

        self.pushButton.clicked.connect(self.search_criteria)
        self.btn_exit_serials.clicked.connect(self.exit)

        # Кнопки Основных критерий

        self.btn_date_DESC_serials.clicked.connect(self.output_of_serials_by_date)
        self.btn_name_DESC_serials.clicked.connect(self.output_of_serials_by_name)
        self.btn_rating_DESC_serials.clicked.connect(self.output_of_serials_by_rating)

        #

    # ----------------------------------------------Основные Критерии---------------------------------------------------
        # №. serial, [rating], (release), style, seasons, description
        # 1. Воскресший Эртугрул, [8.2], 2014-12-10, (боевик), 5, |Описание|

        count = 1
        self.table_serials.appendPlainText("№. serial, [rating], (release), style, seasons, |description|\n")
        for value in sql.execute("SELECT * FROM data_serials ORDER BY release DESC"):
            self.table_serials.appendPlainText(f'{count}. '
                                               f'{value[0]}, '
                                               f'[{value[1]}], '
                                               f'{value[2]}, '
                                               f'({value[3]}), '
                                               f'{value[4]}, '
                                               f'\nОписание: |{value[5]}|\n')
            count += 1

    def output_of_serials_by_rating(self):
        self.table_serials.clear()
        self.table_serials.appendPlainText("№. serial, [rating], (release), style, seasons, |description|\n")
        if len(self.data_criteria_serials) > 0:
            count = 1
            for value in sql.execute(f"""
                    SELECT * FROM data_serials WHERE style in {self.sort()} ORDER BY rating DESC"""):
                self.table_serials.appendPlainText(f'{count}. '
                                                   f'{value[0]}, '
                                                   f'[{value[1]}], '
                                                   f'{value[2]}, '
                                                   f'({value[3]}), '
                                                   f'{value[4]}, '
                                                   f'\nОписание: |{value[5]}|\n')
                count += 1
        else:
            count = 1
            for value in sql.execute("SELECT * FROM data_serials ORDER BY rating DESC"):
                self.table_serials.appendPlainText(f'{count}. '
                                                   f'{value[0]}, '
                                                   f'[{value[1]}], '
                                                   f'{value[2]}, '
                                                   f'({value[3]}), '
                                                   f'{value[4]}, '
                                                   f'\nОписание: |{value[5]}|\n')
                count += 1

    def output_of_serials_by_date(self):
        self.table_serials.clear()
        self.table_serials.appendPlainText("№. serial, [rating], (release), style, seasons, |description|\n")
        if len(self.data_criteria_serials) > 0:
            count = 1
            for value in sql.execute(f"""
                    SELECT * FROM data_serials WHERE style in {self.sort()} ORDER BY release DESC"""):
                self.table_serials.appendPlainText(f'{count}. '
                                                   f'{value[0]}, '
                                                   f'[{value[1]}], '
                                                   f'{value[2]}, '
                                                   f'({value[3]}), '
                                                   f'{value[4]}, '
                                                   f'\nОписание: |{value[5]}|\n')
                count += 1
        else:
            count = 1
            for value in sql.execute("SELECT * FROM data_serials ORDER BY release DESC"):
                self.table_serials.appendPlainText(f'{count}. '
                                                   f'{value[0]}, '
                                                   f'[{value[1]}], '
                                                   f'{value[2]}, '
                                                   f'({value[3]}), '
                                                   f'{value[4]}, '
                                                   f'\nОписание: |{value[5]}|\n')
                count += 1

    def output_of_serials_by_name(self):
        self.table_serials.clear()
        self.table_serials.appendPlainText("№. serial, [rating], (release), style, seasons, |description|\n")
        if len(self.data_criteria_serials) > 0:
            count = 1
            for value in sql.execute(f"""
                    SELECT * FROM data_serials WHERE style in {self.sort()} ORDER BY serial ASC"""):
                self.table_serials.appendPlainText(f'{count}. '
                                                   f'{value[0]}, '
                                                   f'[{value[1]}], '
                                                   f'{value[2]}, '
                                                   f'({value[3]}), '
                                                   f'{value[4]}, '
                                                   f'\nОписание: |{value[5]}|\n')
                count += 1
        else:
            count = 1
            for value in sql.execute("""
                    SELECT * FROM data_serials ORDER BY serial ASC"""):
                self.table_serials.appendPlainText(f'{count}. '
                                                   f'{value[0]}, '
                                                   f'[{value[1]}], '
                                                   f'{value[2]}, '
                                                   f'({value[3]}), '
                                                   f'{value[4]}, '
                                                   f'\nОписание: |{value[5]}|\n')
                count += 1

    # --------------------------------------------Сортировка Критерий---------------------------------------------------

    # Входные данные: {'Фантастика', 'Ужасы'}
    # Возращает: ('Фантастика', 'Ужасы')
    # Нужно для команды в базу данных и для избежание не верных выводов данных
    # SELECT * FROM data WHERE style in ('Фантастика', 'Ужасы')

    def sort(self):
        return f'''('{"', '".join(self.data_criteria_serials)}')'''

    def serials_sort(self, state):
        if state:
            self.data_criteria_serials.add(self.sender().text())
        else:
            self.data_criteria_serials.remove(self.sender().text())

    def search_criteria(self):
        self.table_serials.clear()
        self.table_serials.appendPlainText("№. serial, [rating], (release), style, seasons, |description|\n")
        count = 1
        for value in sql.execute(f"SELECT * FROM data_serials WHERE style in {self.sort()} ORDER BY rating DESC"):
            self.table_serials.appendPlainText(f'{count}. '
                                               f'{value[0]}, '
                                               f'[{value[1]}], '
                                               f'({value[2]}), '
                                               f'{value[3]}, '
                                               f'{value[4]}, '
                                               f'\nОписание: |{value[5]}|\n')
            count += 1

    # ------------------------------------------------------------------------------------------------------------------

    def exit(self):
        serial.close()
        ex.show()


class BooksComics(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('books_comics.ui', self)

        self.data_criteria_books = set()

        # Кнопки Основных критерий

        self.btn_date_DESC_books.clicked.connect(self.output_of_books_by_date)
        self.btn_name_DESC_books.clicked.connect(self.output_of_books_by_name)

        self.btn_exit.clicked.connect(self.exit)

        # Критерии

        self.checkBox.clicked.connect(self.serials_sort)
        self.checkBox_2.clicked.connect(self.serials_sort)
        self.checkBox_3.clicked.connect(self.serials_sort)
        self.checkBox_4.clicked.connect(self.serials_sort)
        self.checkBox_5.clicked.connect(self.serials_sort)

        self.pushButton.clicked.connect(self.search_criteria)

        # №. book_name, [release], author, (style), |toms|
        # 4. Восхождение Героя Щита. Том 11, [2021], Кю Айя, (Манга), |12|

        count = 1
        self.table_books.appendPlainText('№. book_name, [release], author, (style), |toms|\n')
        for value in sql.execute("SELECT * FROM data_books ORDER BY release DESC"):
            self.table_books.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'{value[2]}, '
                                             f'({value[3]}), '
                                             f'|{value[4]}|\n')
            count += 1
    # ----------------------------------------------Основные Критерии---------------------------------------------------

    def output_of_books_by_date(self):
        self.table_books.clear()
        self.table_books('№. book_name, [release], author, (style), |toms|\n')
        count = 1
        if len(self.data_criteria_books) > 0:
            for value in sql.execute(f"SELECT * FROM data_books WHERE style in {self.sort()} ORDER BY release DESC"):
                self.table_books.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'({value[2]}), '
                                                 f'{value[3]}, '
                                                 f'|{value[4]}|\n')
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data_books ORDER BY release DESC"):
                self.table_books.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'{value[2]}, '
                                                 f'({value[3]}), '
                                                 f'|{value[4]}|\n')
                count += 1

    def output_of_books_by_name(self):
        self.table_books.clear()
        self.table_books('№. book_name, [release], author, (style), |toms|\n')
        count = 1
        if len(self.data_criteria_books) > 0:
            for value in sql.execute(f"SELECT * FROM data_books WHERE style in {self.sort()} ORDER BY book_name ASC"):
                self.table_books.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'({value[2]}), '
                                                 f'{value[3]}, '
                                                 f'|{value[4]}|\n')
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data_books ORDER BY book_name ASC"):
                self.table_books.appendPlainText(f'{count}. '
                                                 f'{value[0]}, '
                                                 f'[{value[1]}], '
                                                 f'{value[2]}, '
                                                 f'({value[3]}), '
                                                 f'|{value[4]}|\n')
                count += 1

    # --------------------------------------------Сортировка Критерий---------------------------------------------------

        # Входные данные: {'Фантастика', 'Ужасы'}
        # Возращает: ('Фантастика', 'Ужасы')
        # Нужно для команды в базу данных и для избежание не верных выводов данных
        # SELECT * FROM data WHERE style in ('Фантастика', 'Ужасы')

    def sort(self):
        return f'''('{"', '".join(self.data_criteria_books)}')'''

    def serials_sort(self, state):
        if state:
            self.data_criteria_books.add(self.sender().text())
        else:
            self.data_criteria_books.remove(self.sender().text())

    def search_criteria(self):
        self.table_books.clear()
        self.table_books.appendPlainText('№. book_name, [release], author, (style), |toms|\n')
        count = 1
        for value in sql.execute(f"SELECT * FROM data_books WHERE style in {self.sort()} ORDER BY release DESC"):
            self.table_books.appendPlainText(f'{count}. '
                                             f'{value[0]}, '
                                             f'[{value[1]}], '
                                             f'({value[2]}), '
                                             f'{value[3]}, '                                              
                                             f'|{value[4]}|\n')
            count += 1

    # ------------------------------------------------------------------------------------------------------------------

    def exit(self):
        books_and_comics.close()
        ex.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
