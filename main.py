import urllib.request
from config import *
from os import remove, listdir
from pytube import YouTube
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QStyle, QMainWindow
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QUrl

# TODO: Увеличить базу данных
# TODO: Улутшить интерфейс программы


class Main(QMainWindow):

    """ Главное окно"""

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

        # Дополнительные кнопки

        self.btn_exit.clicked.connect(self._exit)
        self.btn_clear_all_images.clicked.connect(self.clear_all_images)

    @staticmethod
    def clear_all_images():

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(filter(lambda p: p.endswith('.png'), directory_images))

        if len(data_on_downloaded_images) > 0:
            for i in data_on_downloaded_images:
                remove(f"data_images/{i}")

    @staticmethod
    def _exit():
        exit(0)

    @staticmethod
    def serial_window():
        ex.close()
        serial.show()

    @staticmethod
    def books_and_comics_window():
        books_and_comics.show()
        ex.close()

    @staticmethod
    def film_window():
        films.show()
        ex.close()


class Films(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi('ui/film.ui', self)

        # Запоминает названия фильма

        self.name_film_global = ''

        self.setWindowIcon(QIcon('icon.png'))
    # --------------------------------------------<Фукции при запуски>--------------------------------------------------

        self.basic_output_films()

    # ---------------------------------------------<Кнопки и интерфейс>-------------------------------------------------

        # Добавляются и удаляются критерии |films_sort| -> Нужно для запроса в базу данных

        self.data_criteria_films = set()

        # Все критерии -> Вывод фильмов по критериям

        self.checkBox.clicked.connect(self.films_sort)
        self.checkBox_2.clicked.connect(self.films_sort)
        self.checkBox_3.clicked.connect(self.films_sort)

        # Основные критерии -> {Рейтинг, По дате, По названию}

        self.btn_rating_DESC_films.clicked.connect(self.output_of_films_by_rating)
        self.btn_date_DESC_films.clicked.connect(self.output_of_films_by_date)
        self.btn_name_DESC_films.clicked.connect(self.output_of_films_by_name)

        # таблица фильмов

        self.table_films.clicked.connect(self.movie_selection_films)

        # Кнопки

        self.btn_exit_films.clicked.connect(self.exit)
        self.btn_clear_film_images.clicked.connect(self.clear_films_images)

        # Нажатие на Enter
        self.input_search_films.returnPressed.connect(self.checking_the_search_film)

        #

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.horizontalSlider_2.sliderMoved.connect(self.set_volume)

        self.mediaPlayer.setVideoOutput(self.widget_2)
        self.pushButton.clicked.connect(self.download_trailer)
        self.pushButton_2.clicked.connect(self.play_video)
        self.pushButton_2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.horizontalSlider.setSliderPosition(0)

        self.mediaPlayer.setVolume(50)

    def download_trailer(self):
        """Функция для отображеия трейлера"""

        """Если пользователь нажал 1 раз то высветиться предупреждение о том что будет загрузка с интернета 
        и нужно будет подождать и если уже потом пользователь нажимает еще раз то проиходит загрузка и сохрание на пк
        и если в следущий раз пользователь нажмет на кпоку видео загрузиться с пк сразу и не будет предупреждений """

        # TODO: Нужно доработать
        # Видео будет на компьютере Причины:
        # ДОлгая загрузка трейлера
        # Если получится то оптимезировать процес и добавить загрузку с интернета

        directory_videos = listdir("data_videos/")
        data_on_downloaded_videos = set(
            filter(lambda p: p.endswith('.mp4') and p.startswith("1"), directory_videos))

        filename = ''
        url_film_trailer = ''

        for value in sql.execute(f"SELECT videos, id FROM data WHERE film = '{self.name_film_global}'"):

            filename = value[1]
            url_film_trailer = value[0]

        if filename + '.mp4' in data_on_downloaded_videos:
            """Функция выводит трейлер с папки скаченных трейлеров на экран пользователю"""
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"data_videos/{filename + '.mp4'}")))
            self.pushButton_2.setEnabled(True)
            self.ready_for_viewing.setText("Трейлер готов к запуску")
        else:
            """Функция выводит трейлер с интернета на экран пользователю"""
            yt = YouTube(url_film_trailer)
            yt = yt.streams.filter(progressive=True, file_extension='').order_by('resolution').desc().first()
            yt.download("data_videos", filename + '.mp4')

            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"data_videos/{filename + '.mp4'}")))
            self.pushButton_2.setEnabled(True)
            self.ready_for_viewing.setText("Трейлер готов к запуску")

    def play_video(self):

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.pushButton_2.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.pushButton_2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.horizontalSlider.setValue(position)

    def duration_changed(self, duration):
        self.horizontalSlider.setRange(0, duration)

    def set_position(self, position):
        self.mediaPlayer.setPosition(position)

    def set_volume(self, position):
        value = self.horizontalSlider_2.value()
        self.mediaPlayer.setVolume(value)
        self.statusbar.showMessage("Громкость " + str(value) + " %")

    # ------------------------<Дополнительные функции /* Для удобства работы с текстом *\>------------------------------

    def the_order_of_output_from_the_database_films(self):

        """Заголовок в котором показан порядок вывода информации"""

        self.table_films.addItem('№. film, [rating], nation, (release), style, age')

    def films_sort(self, state):

        """Добавление и удалений из множества категорий так же сразу осуществляется сортировка"""

        if state:
            self.data_criteria_films.add(self.sender().text())
        else:
            self.data_criteria_films.remove(self.sender().text())

        self.search_criteria_films()

    def creating_request_films(self):

        """
        Входные данные : Множество жанров -> {"Фантастика", "Ужасы"}
        Возращает запрос в базу данных -> ("Фантастика", "Ужасы")

        Пример выполняемого запроса:
        SELECT * FROM data WHERE style in ("Фантастика", "Ужасы")
        SELECT * FROM <БД> WHERE <Выбранная ячейка> in <Ищем>
        """

        return f'''('{"', '".join(self.data_criteria_films)}')'''

    def table_film_add_item_films(self, value, count):

        """Вывод фильмов и краткой инфмормации в таблицу"""

        self.table_films.addItem(f'{count}. '
                                 f'{value[0]}, '
                                 f'{value[1]}, '
                                 f'[{value[2]}], '
                                 f'({value[3]}), '
                                 f'{value[4]}, '
                                 f'{value[5]}')

    def checking_the_search_film(self):

        """

        Функция дял проверки запроса на поиск ->
        Если фильм не найден то фукция убирает все и пишет "Фильм не найден".
        Если найден фильм то выводтся подробная информация.

        """

        # TODO: Добавить в подробную информацию -> чей фильм
        # TODO: Улучишь поиск чтобы он мог искать не только по названию, но и по главным ролям. ->
        # Если будет сделано то нужно не забыть выводить главных герояв в подробной информаци
        # !!!ВАЖНО!!! Должно происходить автоматически

        film = self.input_search_films.text().strip().capitalize()

        verification_film = sql.execute(f'SELECT film FROM data WHERE film = "{film}"')
        if verification_film.fetchone() is None:
            self.image_films.setText("Фильм не найден....")
            self.table_description_films.clear()
            self.output_rating_films.setText('')
            self.output_age_films.setText('')
            self.output_date_films.setText('')
            self.output_nation_films.setText('')
            self.output_style_films.setText('')
            self.name_film.setText('')
            self.table_description_films.appendPlainText('')

        else:
            self.information_output_films(film)

    def search_for_data_in_the_database_film(self, sorting, type_sorting):

        """Функция для поиска данных в базе данных и вывода в таблицу"""

        self.table_films.clear()
        self.the_order_of_output_from_the_database_films()
        count = 1
        if len(self.data_criteria_films) > 0:
            for value in sql.execute(f"""
                     SELECT * FROM data
                     WHERE style in {self.creating_request_films()}
                     ORDER BY {sorting} {type_sorting}"""):
                self.table_film_add_item_films(value, count)
                count += 1
        else:
            for value in sql.execute(f"""
                     SELECT * FROM data
                     ORDER BY {sorting} {type_sorting}"""):
                self.table_film_add_item_films(value, count)
                count += 1

    # ----------------------------------------------<Базовый вывод>-----------------------------------------------------

    def basic_output_films(self):

        count = 1
        self.table_films.addItem('№. film, [rating], nation, (release), style, age')
        for value in sql.execute("SELECT * FROM data ORDER BY rating DESC"):
            self.table_film_add_item_films(value, count)
            count += 1

    # --------------------------------<Функции для вывода подробной информации фильма>----------------------------------

    def movie_selection_films(self):

        """Получаем выбранный фильм и редактируем под запрос"""

        selected_movie = self.table_films.currentItem().text()[3:].split(", ")
        if selected_movie[1] != 'film':
            self.information_output_films(selected_movie[1])

    def information_output_films(self, image_name):

        """Функция для подробной информации по выбранному фильму"""

        # Таблица data - Фильмы
        # id TEXT 1000001 (id нужно для простого сохранение фотографий)
        # film TEXT Шан-Чи и легенда десяти колец
        # rating REAL 9.1
        # nation TEXT США
        # release DATE 2021-05-09
        # style TEXT Фантастика
        # age TEXT 16+
        # (TODO: age Изменить на число и выводить потом со знаком + для того что бы было использованно меньше памяти)
        # description TEXT Описание
        # images TEXT (images хранит ссылку для скачивание изображение с интерета используется библиотка urllib.request)

        self.table_description_films.clear()
        self.ready_for_viewing.setText(" ")
        self.name_film_global = image_name

        for value in sql.execute(f"SELECT * FROM data WHERE film = '{image_name}'"):

            # Изображение

            self.downloading_an_image_from_the_internet_films(value[8], value[0])

            # Остальная информация

            self.output_rating_films.setText(f'{value[1]}')
            self.output_age_films.setText(f'{value[5]}')
            self.output_date_films.setText(f'{value[4]}')
            self.output_nation_films.setText(f'{value[2]}')
            self.output_style_films.setText(f'{value[3]}')
            self.name_film.setText(f'{value[0]}')
            self.table_description_films.appendPlainText(f'{value[6]}')

    @staticmethod
    def clear_films_images():

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(filter(lambda p: p.endswith('.png') and p.startswith("1"), directory_images))

        for image in data_on_downloaded_images:
            if "1" == image[:1]:
                remove(f"data_images/{image}")

    def downloading_an_image_from_the_internet_films(self, url, id_film):

        """
        Фунцкия для скачивания изображения с интернета и так же она сохраняет изображение с интернета
        на компьютере пользователя более подробное описание ниже ->

        После того как пользователь выбрал фильм скачивается изображение с интернета
        Так происходит каждый раз, загрузка немного тормозит программу
        Поэтому можно реализовать функцию которая после выбранного фильма скачивает изображение с интернета и
        сохранят на пк -> Тем самым после того как пользователь выберет этот фильм снова , он загрузится моментально

        В базе данных добавить столбец id -> 1000001, 1000002, 1000003
        Потом скачивается в папку под этим id и можно будет открывать изображение
        Будет несколько типов:
        1. 1000001 - Фильмы (Не будет изменений)
        2. 2000001 - Сериалы (Возможны изменения)
        3. 3000001 - Книги (Возможно изменение)
        """

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(filter(lambda p: p.endswith('.png') and p.startswith("1"), directory_images))

        if id_film + ".png" in data_on_downloaded_images:
            pixmap = QPixmap(f"data_images/{id_film}.png")
            self.image_films.setPixmap(pixmap)
        else:
            data = urllib.request.urlopen(url).read()

            f = open(f"data_images/{id_film}.png", "wb")
            f.write(data)
            f.close()

            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.image_films.setPixmap(pixmap)

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

    def output_of_films_by_rating(self):

        """Вывод фильмов по рейтингу"""

        self.search_for_data_in_the_database_film("rating", "DESC")

    def output_of_films_by_date(self):

        """Вывод фильмов по дате релиза"""

        self.search_for_data_in_the_database_film("release", "DESC")

    def output_of_films_by_name(self):

        """Вывод фильмов по названию"""

        self.search_for_data_in_the_database_film("film", "ASC")

    def search_criteria_films(self):

        """Сортировка по критериям"""

        self.search_for_data_in_the_database_film("rating", "DESC")

    #  -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def exit():
        films.close()
        ex.show()


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

    def checking_the_search_serials(self):

        """

            Функция дял проверки запроса на поиск ->
            Если фильм не найден то фукция убирает все и пишет "Фильм не найден".
            Если найден фильм то выводтся подробная информация.

        """

        # TODO: Добавить в подробную информацию -> чей фильм
        # TODO: Улучишь поиск чтобы он мог искать не только по названию, но и по главным ролям. ->
        # Если будет сделано то нужно не забыть выводить главных герояв в подробной информаци
        # !!!ВАЖНО!!! Должно происходить автоматически

        film = self.input_search_serials.text().strip().capitalize()

        verification_film = sql.execute(f'SELECT film FROM data_serials WHERE film = "{film}"')

        if verification_film.fetchone() is None:

            self.image_serial.setText("Фильм не найден....")
            self.table_description_serial.clear()
            self.output_rating_serial.setText('')
            self.output_age_serial.setText('')
            self.output_date_serial.setText('')
            self.output_nation_serial.setText('')
            self.output_style_serial.setText('')
            self.name_serial.setText('')
            self.table_description_serial.appendPlainText('')

        else:
            self.information_output_serials(film)

    def serials_sort(self, state):
        if state:
            self.data_criteria_serials.add(self.sender().text())
        else:
            self.data_criteria_serials.remove(self.sender().text())

        self.search_criteria_serials()

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

        """Вывод сериалов и краткой информации в таблицу"""

        self.table_serials.addItem(f'{count}. '
                                   f'{value[0]}, '
                                   f'{value[1]}, '
                                   f'[{value[2]}], '
                                   f'({value[3]}), '
                                   f'{value[4]}, '
                                   f'{value[5]}, '
                                   f'|{value[6]}|')

    def checking_the_search_serial(self):

        """

        Функция дял проверки запроса на поиск ->
        Если сериал не найден то фукция убирает все и пишет "Сериал не найден".
        Если найден сериал то выводтся подробная информация.

        """
        pass

    def search_for_data_in_the_database_serials(self, sorting, type_sorting):

        """Функция для поиска данных в базе данных и вывода в таблицу"""

        self.table_serials.clear()
        self.the_order_of_output_from_the_database_serials()
        count = 1
        if len(self.data_criteria_serials) > 0:
            for value in sql.execute(f"""
                     SELECT * FROM data_serials
                     WHERE style in {self.creating_request_serials()}
                     ORDER BY {sorting} {type_sorting}"""):
                self.table_film_add_item_serials(value, count)
                count += 1
        else:
            for value in sql.execute(f"""
                     SELECT * FROM data_serials
                     ORDER BY {sorting} {type_sorting}"""):
                self.table_film_add_item_serials(value, count)
                count += 1

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
        if selected_movie_serials[1] != 'serials':
            self.information_output_serials(selected_movie_serials[1])

    def information_output_serials(self, image_name):

        self.table_description_serials.clear()

        for value in sql.execute(f"SELECT * FROM data_serials WHERE serial = '{image_name}'"):

            self.downloading_an_image_from_the_internet_serials(value[-1], value[0])

            # Остальная информация

            self.output_rating_serials.setText(f'{value[1]}')
            self.output_age_serials.setText(f'{value[5]}')
            self.output_data_serials.setText(f'{value[3]}')
            self.output_nation_serials.setText(f'{value[2]}')
            self.output_style_serials.setText(f'{value[4]}')
            self.name_film.setText(f'{value[0]}')
            self.table_description_serials.appendPlainText(f'{value[7]}')

    @staticmethod
    def clear_serials_images():

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(filter(lambda p: p.endswith('.png') and p.startswith("2"), directory_images))

        for image in data_on_downloaded_images:
            if "2" == image[:1]:
                remove(f"data_images/{image}")

    def downloading_an_image_from_the_internet_serials(self, url_name, id_serial):

        """
        Фунцкия для скачивания изображения с интернета и так же она сохраняет изображение с интернета
        на компьютере пользователя более подробное описание ниже ->

        После того как пользователь выбрал фильм скачивается изображение с интернета
        Так происходит каждый раз, загрузка немного тормозит программу
        Поэтому можно реализовать функцию которая после выбранного фильма скачивает изображение с интернета и
        сохранят на пк -> Тем самым после того как пользователь выберет этот фильм снова , он загрузится моментально

        В базе данных добавить столбец id -> 1000001, 1000002, 1000003
        Потом скачивается в папку под этим id и можно будет открывать изображение
        Будет несколько типов:
        1. 1000001 - Фильмы (Не будет изменений)
        2. 2000001 - Сериалы (Возможны изменения)
        3. 3000001 - Книги (Возможно изменение)
        """

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(filter(lambda p: p.endswith('.png') and p.startswith("2"), directory_images))

        if id_serial + ".png" in data_on_downloaded_images:

            pixmap = QPixmap(f"data_images/{id_serial}.png")
            self.image_serial.setPixmap(pixmap)

        else:

            data = urllib.request.urlopen(url_name).read()

            f = open(f"data_images/{id_serial}.png", "wb")
            f.write(data)
            f.close()

            pixmap = QPixmap()
            pixmap.loadFromData(data)
            self.image_serial.setPixmap(pixmap)

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

    def output_of_serials_by_rating(self):

        """Вывод сериалов по рейтингу"""

        self.search_for_data_in_the_database_serials("rating", "DESC")

    def output_of_serials_by_date(self):

        """Вывод сериалов по дате релиза"""

        self.search_for_data_in_the_database_serials("release", "DESC")

    def output_of_serials_by_name(self):

        """Вывод сериалов по названию"""

        self.search_for_data_in_the_database_serials("serial", "ASC")

    def search_criteria_serials(self):

        """Сортировка по критериям"""

        self.search_for_data_in_the_database_serials("rating", "DESC")

    # ------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def exit():
        serial.close()
        ex.show()


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
        ex.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec())
