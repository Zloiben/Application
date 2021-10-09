import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from translate import Translator

# ----------------------------------------------<База Данных>-----------------------------------------------------------

import sqlite3

db = sqlite3.connect("database.db")
sql = db.cursor()

# --------------------------------<Данные возращаемы с базы данных Сериалов>--------------------------------------------
# serial = 'Test'
# rating = 0 - 10
# release = 'YYYY-MM-DD'
# style = 'Test'
# seasons = 0 - n
# description = 'Test' -> Описание
# --------------------------------<Данные возращаемы с базы данных Книг>------------------------------------------------
# book_name = 'Test'
# release = 'YYYY'
# author = 'Test'
# style = 'Test'
# toms = 0 - n , Количесвто томов или частей у книги
# --------------------------------<Данные возращаемы с базы данных Фильмов>---------------------------------------------
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

# ----------------------------------------------------------------------------------------------------------------------

# TODO: Увеличить базу данных
# TODO: Улутшить интерфейс программы


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        # Классы приложений -> Нужны для перехода между окнами

        global the_world_of_books_movies_and_series, translator

        the_world_of_books_movies_and_series = TheWorldOfBooksMoviesAndSeries()
        translator = TranslatorApp()

        #

        uic.loadUi("ui/main_main.ui", self)

        # Кнопки

        self.pushButton.clicked.connect(self.translator_window)
        self.pushButton_2.clicked.connect(self.the_world_of_books_movies_and_series_window)

    @staticmethod
    def the_world_of_books_movies_and_series_window():
        the_world_of_books_movies_and_series.show()
        ex.close()

    @staticmethod
    def translator_window():
        translator.show()
        ex.close()


class TranslatorApp(QMainWindow):

    # TODO: Переделать переводчик

    """ Переводчик Используется библиотека """

    def __init__(self):
        super().__init__()

        #

        uic.loadUi('ui/translation.ui', self)

        #

        self.btn_translation.clicked.connect(self.translation)
        self.btn_clear.clicked.connect(self.clear_table)

        #

    def translation(self):
        FROM_LANGUAGE = self.comboBox.currentText().split('-')
        TO_LANGUAGE = self.comboBox_2.currentText()
        TEXT = self.textEdit.toPlainText()

        translator = Translator(from_lang=FROM_LANGUAGE[0], to_lang=TO_LANGUAGE)

        result = translator.translate(TEXT)

        self.plainTextEdit_2.appendPlainText(result)

    def clear_table(self):
        self.textEdit.clear()
        self.plainTextEdit_2.clear()


class TheWorldOfBooksMoviesAndSeries(QMainWindow):

    """ Главное окно 'Мир книг, фильмов, сериалов' """

    def __init__(self):
        super().__init__()

        # Классы критерий

        global serial, films, books_and_comics

        films = Films()
        serial = Serials()
        books_and_comics = BooksComics()

        #

        uic.loadUi('ui/main.ui', self)

        # Кнопки перехода в другое окно

        self.btn_films.clicked.connect(self.film_window)
        self.btn_serials.clicked.connect(self.serial_window)
        self.btn_books_and_comics.clicked.connect(self.books_and_comics_window)

        # Кнопка назад

        self.btn_exit_main.clicked.connect(self.exit)

    @staticmethod
    def serial_window():
        the_world_of_books_movies_and_series.close()
        serial.show()

    @staticmethod
    def books_and_comics_window():
        books_and_comics.show()
        the_world_of_books_movies_and_series.close()

    @staticmethod
    def film_window():
        films.show()
        the_world_of_books_movies_and_series.close()

    @staticmethod
    def exit():
        the_world_of_books_movies_and_series.close()
        ex.show()


class Films(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/film.ui', self)

    # ----------------------------------------------<Идеи для добавления>-----------------------------------------------

        # TODO: Улучишь поиск чтобы он мог искать не только по названию, но и по главным ролям. ->
        # Если будет сделано то нужно не забыть выводить главных герояв в подробной информации

        # TODO: Добавить в подробную информацию -> чей фильм

    # --------------------------------------------<Фукции при запуски>--------------------------------------------------

        self.basic_output()

    # ---------------------------------------------<Кнопки>-------------------------------------------------------------

        # Добавляются и удаляются критерии |films_sort| -> Нужно для запроса в базу данных

        self.data_criteria = set()

        # Все критерии -> Вывод фильмов по критериям
        # TODO: Требуется добавить критериев /* Вся информация берется с кинопоиска *\

        self.checkBox.clicked.connect(self.films_sort)
        self.checkBox_2.clicked.connect(self.films_sort)
        self.checkBox_3.clicked.connect(self.films_sort)

        # Основные критерии -> {Рейтинг, По дате, По названию}

        self.btn_rating_DESC_films.clicked.connect(self.output_of_films_by_rating)
        self.btn_date_DESC_films.clicked.connect(self.output_of_films_by_date)
        self.btn_name_DESC_films.clicked.connect(self.output_of_films_by_name)

        # Кнопка выхода -> Возращает на предыдущие окно

        self.btn_exit_films.clicked.connect(self.exit)

        # Кнопка поиска по введенному фильму

        self.search_btn.clicked.connect(self.search)

        # Кнопка нужна для вывода подробной информации -> При нажатии на фильм будет выведина полная информация

        self.table_films.clicked.connect(self.movie_selection)

    # ------------------------<Дополнительные функции /* Для удобства работы с текстом *\>------------------------------

    def the_order_of_output_from_the_database(self):
        self.table_films.addItem('№. film, [rating], nation, (release), style, age')

    def creating_request(self):

        # Входные данные множество жанров -> {'Фантастика', 'Ужасы'}
        # Возращает для отправки запроса в базу данных -> ('Фантастика', 'Ужасы')
        # Пример запроса:
        # SELECT * FROM data WHERE style in ('Фантастика', 'Ужасы')

        return f'''('{"', '".join(self.data_criteria)}')'''

    def table_film_add_item(self, value, count):
        self.table_films.addItem(f'{count}. '
                                 f'{value[0]}, '
                                 f'[{value[1]}], '
                                 f'{value[2]}, '
                                 f'({value[3]}), '
                                 f'{value[4]}, '
                                 f'{value[5]}')

    # ----------------------------------------------<Базовый вывод>-----------------------------------------------------

    def basic_output(self):
        count = 1
        self.the_order_of_output_from_the_database()
        for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
            self.table_film_add_item(value, count)
            count += 1

    # --------------------------------<Функции для вывода подробной информации фильма>----------------------------------

    def movie_selection(self):
        selected_movie = self.table_films.currentItem().text()[3:].split(", ")
        # -> ['Шан-Чи и легенда десяти колец', '[7.3]', 'США', '(Фантастика)', 16+]
        if selected_movie[0] != 'film':
            self.information_output(selected_movie[0])

    def information_output(self, image_name):

        self.table_description.clear()

        for value in sql.execute(f"SELECT * FROM data WHERE film = '{image_name}'"):

            # Изображение

            pixmap = QPixmap('images_data/' + f'{value[7]}')
            self.image.setPixmap(pixmap)

            # Остальная информация

            self.output_rating.setText(f'{value[1]}')
            self.output_age.setText(f'{value[5]}')
            self.output_date.setText(f'{value[4]}')
            self.output_nation.setText(f'{value[2]}')
            self.output_style.setText(f'{value[3]}')
            self.name_film.setText(f'{value[0]}')
            self.table_description.appendPlainText(f'{value[6]}')

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

    def output_of_films_by_rating(self):
        self.table_films.clear()
        self.the_order_of_output_from_the_database()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                    SELECT * FROM data WHERE style in {self.creating_request()} ORDER BY rating DESC"""):
                self.table_film_add_item(value, count)
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
                self.table_film_add_item(value, count)
                count += 1

    def output_of_films_by_date(self):
        self.table_films.clear()
        self.the_order_of_output_from_the_database()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                        SELECT * FROM data WHERE style in {self.creating_request()} ORDER BY release DESC"""):
                self.table_film_add_item(value, count)
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY release DESC"):
                self.table_film_add_item(value, count)
                count += 1

    def output_of_films_by_name(self):
        self.table_films.clear()
        self.the_order_of_output_from_the_database()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                                    SELECT * FROM data WHERE style in {self.creating_request()} ORDER BY film ASC"""):
                self.table_film_add_item(value, count)
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY film ASC"):
                self.table_film_add_item(value, count)
                count += 1

    # --------------------------------------------Сортировка по Критериям-----------------------------------------------

    def search(self):
        self.information_output(self.input_search.text())

    def films_sort(self, state):

        # Добавление и удалений из множества категорий так же сразу осуществляется сортировка

        if state:
            self.data_criteria.add(self.sender().text())
        else:
            self.data_criteria.remove(self.sender().text())

        self.search_criteria()

    def search_criteria(self):

        # Поиск по критериям

        self.table_films.clear()
        self.the_order_of_output_from_the_database()
        count = 1
        for value in sql.execute(f"SELECT * FROM data WHERE style in {self.creating_request()} ORDER BY rating DESC"):
            self.table_film_add_item(value, count)
            count += 1

    #  -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def exit():
        films.close()
        the_world_of_books_movies_and_series.show()


class Serials(QMainWindow):

    # TODO: Сделал пример -> нужно переделать под сериалы

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/serials.ui', self)

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

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

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

    @staticmethod
    def exit():
        serial.close()
        the_world_of_books_movies_and_series.show()


class BooksComics(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/books_comics.ui', self)

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
        self.table_books.appendPlainText('№. book_name, [release], author, (style), |toms|\n')
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
        self.table_books.appendPlainText('№. book_name, [release], author, (style), |toms|\n')
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

    # --------------------------------------------<Сортировка Критерий>-------------------------------------------------

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

    @staticmethod
    def exit():
        books_and_comics.close()
        the_world_of_books_movies_and_series.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
