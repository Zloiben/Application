import sys
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import urllib.request
import sqlite3

db = sqlite3.connect("database.db")
sql = db.cursor()

# TODO: Увеличить базу данных
# TODO: Улутшить интерфейс программы


class Main(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icon.png'))

        # Классы приложений -> Нужны для перехода между окнами

        global the_world_of_books_movies_and_series

        the_world_of_books_movies_and_series = TheWorldOfBooksMoviesAndSeries()

        #

        uic.loadUi("ui/main_main.ui", self)

        # Кнопки
        self.pushButton_2.clicked.connect(self.the_world_of_books_movies_and_series_window)

    @staticmethod
    def the_world_of_books_movies_and_series_window():
        the_world_of_books_movies_and_series.show()
        ex.close()


class TheWorldOfBooksMoviesAndSeries(QMainWindow):

    """ Главное окно 'Мир книг, фильмов, сериалов' """

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icon.png'))

        #

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

        self.setWindowIcon(QIcon('icon.png'))

    # ----------------------------------------------<Идеи для добавления>-----------------------------------------------

        # TODO: Улучишь поиск чтобы он мог искать не только по названию, но и по главным ролям. ->
        # Если будет сделано то нужно не забыть выводить главных герояв в подробной информации

        # TODO: Добавить в подробную информацию -> чей фильм

    # --------------------------------------------<Фукции при запуски>--------------------------------------------------

        self.basic_output_films()

    # ---------------------------------------------<Кнопки и интерфейс>-------------------------------------------------

        # Добавляются и удаляются критерии |films_sort| -> Нужно для запроса в базу данных

        self.data_criteria = set()

        # Все критерии -> Вывод фильмов по критериям

        self.checkBox.clicked.connect(self.films_sort)
        self.checkBox_2.clicked.connect(self.films_sort)
        self.checkBox_3.clicked.connect(self.films_sort)

        # Основные критерии -> {Рейтинг, По дате, По названию}

        self.btn_rating_DESC_films.clicked.connect(self.output_of_films_by_rating)
        self.btn_date_DESC_films.clicked.connect(self.output_of_films_by_date)
        self.btn_name_DESC_films.clicked.connect(self.output_of_films_by_name)

        # Кнопки

        self.btn_exit_films.clicked.connect(self.exit)
        self.btn_search_films.clicked.connect(self.checking_the_search)

        # Кнопка нужна для вывода подробной информации -> При нажатии на фильм будет выведина полная информация

        self.table_films.clicked.connect(self.movie_selection_films)

    # ------------------------<Дополнительные функции /* Для удобства работы с текстом *\>------------------------------

    def the_order_of_output_from_the_database_films(self):
        self.table_films.addItem('№. film, [rating], nation, (release), style, age')

    def creating_request_films(self):

        """
        Входные данные : Множество жанров -> {"Фантастика", "Ужасы"}
        Возращает запрос в базу данных -> ("Фантастика", "Ужасы")

        Пример выполняемого запроса:
        SELECT * FROM data WHERE style in ("Фантастика", "Ужасы")
        SELECT * FROM <БД> WHERE <Выбранная ячейка> in <Ищем>
        """

        return f'''('{"', '".join(self.data_criteria)}')'''

    def table_film_add_item_films(self, value, count):

        """
        Вывод фильмов и краткой инфмормации инфмормации
        """

        self.table_films.addItem(f'{count}. '
                                 f'{value[0]}, '
                                 f'[{value[1]}], '
                                 f'{value[2]}, '
                                 f'({value[3]}), '
                                 f'{value[4]}, '
                                 f'{value[5]}')

    def checking_the_search(self):

        """

        Функция дял проверки запроса -> Если фильм не найден то фукция убирает все и пишет "Фильм не найден"
        Если найден фильм то выводтся подробная информация

        """

        film = self.input_search_films.text()

        verification_film = sql.execute(f'SELECT * FROM data WHERE film = "{film}"')
        if verification_film.fetchone() is None:
            self.table_description_films.clear()
            self.image_films.setText("Фильм не найден....")
            self.output_rating_films.setText('')
            self.output_age_films.setText('')
            self.output_date_films.setText('')
            self.output_nation_films.setText('')
            self.output_style_films.setText('')
            self.name_film.setText('')
            self.table_description_films.appendPlainText('')
        else:
            self.information_output_films(film)

    # ----------------------------------------------<Базовый вывод>-----------------------------------------------------

    def basic_output_films(self):
        count = 1
        self.the_order_of_output_from_the_database_films()
        for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
            self.table_film_add_item_films(value, count)
            count += 1

    # --------------------------------<Функции для вывода подробной информации фильма>----------------------------------

    def movie_selection_films(self):
        selected_movie = self.table_films.currentItem().text()[3:].split(", ")
        # -> ['Шан-Чи и легенда десяти колец', '[7.3]', 'США', '(Фантастика)', 16+]
        if selected_movie[0] != 'film':
            self.information_output_films(selected_movie[0])

    def information_output_films(self, image_name):

        """

        Функция для подробной информации по выбранному фильму

        """

        self.table_description_films.clear()

        for value in sql.execute(f"SELECT * FROM data WHERE film = '{image_name}'"):

            self.downloading_an_image_from_the_internet_films(value[7])

            # Остальная информация

            self.output_rating_films.setText(f'{value[1]}')
            self.output_age_films.setText(f'{value[5]}')
            self.output_date_films.setText(f'{value[4]}')
            self.output_nation_films.setText(f'{value[2]}')
            self.output_style_films.setText(f'{value[3]}')
            self.name_film.setText(f'{value[0]}')
            self.table_description_films.appendPlainText(f'{value[6]}')

    def downloading_an_image_from_the_internet_films(self, url_name):

        """

        Фунцкия для скачивая изображения с интернета

        """

        data = urllib.request.urlopen(url_name).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.image_films.setPixmap(pixmap)

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

    def output_of_films_by_rating(self):
        self.table_films.clear()
        self.the_order_of_output_from_the_database_films()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                    SELECT * FROM data WHERE style in {self.creating_request_films()} ORDER BY rating DESC"""):
                self.table_film_add_item_films(value, count)
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
                self.table_film_add_item_films(value, count)
                count += 1

    def output_of_films_by_date(self):
        self.table_films.clear()
        self.the_order_of_output_from_the_database_films()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                        SELECT * FROM data WHERE style in {self.creating_request_films()} ORDER BY release DESC"""):
                self.table_film_add_item_films(value, count)
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY release DESC"):
                self.table_film_add_item_films(value, count)
                count += 1

    def output_of_films_by_name(self):
        self.table_films.clear()
        self.the_order_of_output_from_the_database_films()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                                SELECT * FROM data WHERE style in {self.creating_request_films()} ORDER BY film ASC"""):
                self.table_film_add_item_films(value, count)
                count += 1
        else:
            for value in sql.execute("SELECT * FROM data ORDER BY film ASC"):
                self.table_film_add_item_films(value, count)
                count += 1

    # --------------------------------------------Сортировка по Критериям-----------------------------------------------

    def search_films(self):
        self.information_output_films(self.input_search_films.text())

    def films_sort(self, state):

        """

        Добавление и удалений из множества категорий так же сразу осуществляется сортировка

        """

        if state:
            self.data_criteria.add(self.sender().text())
        else:
            self.data_criteria.remove(self.sender().text())

        self.search_criteria_films()

    def search_criteria_films(self):

        """ Сортировка по критериям """

        self.table_films.clear()
        self.the_order_of_output_from_the_database_films()
        count = 1
        for value in sql.execute(f"""
                            SELECT * FROM data WHERE style in {self.creating_request_films()} ORDER BY rating DESC"""):
            self.table_film_add_item_films(value, count)
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

        self.setWindowIcon(QIcon('icon.png'))

        self.basic_output_serials()

    # ---------------------------------------------<Кнопки и интерфейс>-------------------------------------------------

        self.data_criteria_serials = set()

        # Критерии

        self.checkBox.clicked.connect(self.serials_sort)
        self.checkBox_2.clicked.connect(self.serials_sort)
        self.checkBox_3.clicked.connect(self.serials_sort)

        # Кнопки

        self.btn_search_serials.clicked.connect(self.search_criteria_serials)
        self.btn_exit_serials.clicked.connect(self.exit)

        # Кнопки Основных критерий

        self.btn_date_DESC_serials.clicked.connect(self.output_of_serials_by_date)
        self.btn_name_DESC_serials.clicked.connect(self.output_of_serials_by_name)
        self.btn_rating_DESC_serials.clicked.connect(self.output_of_serials_by_rating)

        # Кнопка нужна для вывода подробной информации -> При нажатии на фильм будет выведина полная информация

        self.table_serials.clicked.connect(self.movie_selection_serials)

    # ------------------------<Дополнительные функции /* Для удобства работы с текстом *\>------------------------------

    def the_order_of_output_from_the_database_serials(self):
        self.table_serials.addItem('№. serials, [rating], nation, (release), style, age, |seasons|')

    def creating_request_serials(self):

        """
        Входные данные : Множество жанров -> {"Фантастика", "Ужасы"}
        Возращает запрос в базу данных -> ("Фантастика", "Ужасы")

        Пример выполняемого запроса:
            SELECT * FROM data WHERE style in ("Фантастика", "Ужасы")
            SELECT * FROM <БД> WHERE <Выбранная ячейка> in <Ищем>
        """

        return f'''('{"', '".join(self.data_criteria_serials)}')'''

    def table_film_add_item_serials(self, value, count):
        self.table_serials.addItem(f'{count}. '
                                   f'{value[0]}, '
                                   f'[{value[1]}], '
                                   f'{value[2]}, '
                                   f'({value[3]}), '
                                   f'{value[4]}, '
                                   f'{value[5]}, '
                                   f'|{value[6]}|')

    # ----------------------------------------------<Базовый вывод>-----------------------------------------------------

    def basic_output_serials(self):
        count = 1
        self.the_order_of_output_from_the_database_serials()
        for value in sql.execute("SELECT * FROM data_serials ORDER BY rating DESC"):
            self.table_film_add_item_serials(value, count)
            count += 1

    # --------------------------------<Функции для вывода подробной информации фильма>----------------------------------

    def movie_selection_serials(self):
        selected_movie_serials = self.table_serials.currentItem().text()[3:].split(", ")
        # -> ['Рик и Морти', '[9.0]', 'США', '(2014-09-08)', 'Мультфильм', '18+', '5']
        if selected_movie_serials[0] != 'serials':
            self.information_output_serials(selected_movie_serials[0])

    def information_output_serials(self, image_name):

        self.table_description_serials.clear()
        for value in sql.execute(f"SELECT * FROM data_serials WHERE serial = '{image_name}'"):

            pixmap = QPixmap('images_data/images_serials/' + f'{value[8]}')
            self.image.setPixmap(pixmap)

            # Остальная информация

            self.output_rating_serials.setText(f'{value[1]}')
            self.output_age_serials.setText(f'{value[5]}')
            self.output_data_serials.setText(f'{value[3]}')
            self.output_nation_serials.setText(f'{value[2]}')
            self.output_style_serials.setText(f'{value[4]}')
            self.name_film.setText(f'{value[0]}')
            self.table_description_serials.appendPlainText(f'{value[7]}')

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

    def output_of_serials_by_rating(self):
        self.table_serials.clear()
        self.the_order_of_output_from_the_database_serials()
        if len(self.data_criteria_serials) > 0:
            count = 1
            for value in sql.execute(f"""
                  SELECT * FROM data_serials WHERE style in {self.creating_request_serials()} ORDER BY rating DESC"""):
                self.table_film_add_item_serials(value, count)
                count += 1
        else:
            count = 1
            for value in sql.execute("SELECT * FROM data_serials ORDER BY rating DESC"):
                self.table_film_add_item_serials(value, count)
                count += 1

    def output_of_serials_by_date(self):
        self.table_serials.clear()
        self.the_order_of_output_from_the_database_serials()
        if len(self.data_criteria_serials) > 0:
            count = 1
            for value in sql.execute(f"""
                  SELECT * FROM data_serials WHERE style in {self.creating_request_serials()} ORDER BY release DESC"""):
                self.table_film_add_item_serials(value, count)
                count += 1
        else:
            count = 1
            for value in sql.execute("SELECT * FROM data_serials ORDER BY release DESC"):
                self.table_film_add_item_serials(value, count)
                count += 1

    def output_of_serials_by_name(self):
        self.table_serials.clear()
        self.the_order_of_output_from_the_database_serials()
        if len(self.data_criteria_serials) > 0:
            count = 1
            for value in sql.execute(f"""
                    SELECT * FROM data_serials WHERE style in {self.creating_request_serials()} ORDER BY serial ASC"""):
                self.table_film_add_item_serials(value, count)
                count += 1
        else:
            count = 1
            for value in sql.execute("""
                    SELECT * FROM data_serials ORDER BY serial ASC"""):
                self.table_film_add_item_serials(value, count)
                count += 1

    # --------------------------------------------Сортировка Критерий---------------------------------------------------

    def serials_sort(self, state):
        if state:
            self.data_criteria_serials.add(self.sender().text())
        else:
            self.data_criteria_serials.remove(self.sender().text())

        self.search_criteria_serials()

    def search_criteria_serials(self):
        self.table_serials.clear()
        self.the_order_of_output_from_the_database_serials()
        count = 1
        for value in sql.execute(f"""
                SELECT * FROM data_serials WHERE style in {self.creating_request_serials()} ORDER BY rating DESC"""):
            self.table_film_add_item_serials(value, count)
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

        self.setWindowIcon(QIcon('icon.png'))

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
