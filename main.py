import urllib.request
from UI_file import Serials_ui, Settings_ui, Books_ui, Film_ui, Main_ui
from os import remove, listdir
import pytube
from pytube import YouTube
import sys
from PyQt5.QtWidgets import QApplication, QStyle, QMainWindow, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QUrl
import sqlite3

db = sqlite3.connect("data_base.db")
sql = db.cursor()


class Main(QMainWindow, Main_ui):

    """ Главное окно"""

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('icon.png'))

        #

        global serial, films, books_and_comics, settings

        films = Films()
        serial = Serials()
        books_and_comics = BooksComics()
        settings = Settings()

        #

        # loadUi('ui/main.ui', self)
        self.setupUi(self)

        # Кнопки перехода в другое окно

        self.btn_films.clicked.connect(self.film_window)
        self.btn_serials.clicked.connect(self.serial_window)
        self.btn_books_and_comics.clicked.connect(self.books_and_comics_window)
        self.btn_settings.clicked.connect(self.setting_window)

        # Дополнительные кнопки

        self.btn_exit.clicked.connect(self._exit)

    @staticmethod
    def _exit():
        db.close()
        exit(0)

    @staticmethod
    def serial_window():
        serial.show()
        ex.close()

    @staticmethod
    def books_and_comics_window():
        books_and_comics.show()
        ex.close()

    @staticmethod
    def film_window():
        films.show()
        films.gui()
        ex.close()

    @staticmethod
    def setting_window():
        settings.show()
        ex.close()

         
class Films(QMainWindow, Film_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.gui()

        # Запоминает названия фильма

        self.name_film_global = ''

        self.setWindowIcon(QIcon('icon.png'))

        # Добавляются и удаляются критерии |films_sort| -> Нужно для запроса в базу данных
        self.data_criteria = set()

        self.basic_by_output()

    # ---------------------------------------------<Кнопки и интерфейс>-------------------------------------------------

        # Все критерии -> Вывод фильмов по критериям

        self.checkBox_9.clicked.connect(self.sort)
        self.checkBox_8.clicked.connect(self.sort)
        self.checkBox_7.clicked.connect(self.sort)
        self.checkBox_6.clicked.connect(self.sort)
        self.checkBox_5.clicked.connect(self.sort)
        self.checkBox_4.clicked.connect(self.sort)
        self.checkBox_3.clicked.connect(self.sort)
        self.checkBox_2.clicked.connect(self.sort)
        self.checkBox.clicked.connect(self.sort)

        # Основные критерии -> {Рейтинг, По дате, По названию}

        self.btn_rating_output.clicked.connect(self.output_by_rating)
        self.btn_date_output.clicked.connect(self.output_by_date)
        self.btn_name_output.clicked.connect(self.output_by_name)

        # таблица фильмов

        self.table_films.clicked.connect(self.movie_selection)

        # Кнопки

        self.btn_exit_films.clicked.connect(self._exit)
        self.btn_clear_film_images.clicked.connect(self.clear_images_confirmation)
        self.btn_clear_trailers.clicked.connect(self.clear_trailers_confirmation)

        # Нажатие Поиска на Enter
        self.input_search_films.returnPressed.connect(self.checking_search)

        #

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.horizontalSlider_2.sliderMoved.connect(self.set_volume)

        self.mediaPlayer.setVideoOutput(self.widget_film_trailer)
        self.pushButton.clicked.connect(self.download_trailer)
        self.pushButton_2.clicked.connect(self.play)
        self.pushButton_2.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.horizontalSlider.setSliderPosition(0)

        self.mediaPlayer.setVolume(50)

    def gui(self):

        # TODO Добавить в БД базу данных на англиском
        # TODO: Переименовать категории
        # TODO: Перенести в другой фаил
        if Settings.get_language() == "Ru":
            self.btn_exit_films.setText("<- Назад")
            self.btn_clear_film_images.setText("Очистить изображения")
            self.btn_clear_trailers.setText("Удалить трейлеры")

            self.btn_date_output.setText("По дате")
            self.btn_name_output.setText("По названию")
            self.btn_rating_output.setText("По рейтингу")

            self.input_search_films.setText("Поиск...")

            self.pushButton.setText("Загрузить трейлер")
            self.label_2.setText("Громкость")

            self.rating_films.setText("Рейтинг:")
            self.nation_films.setText("Страна:")
            self.style_films.setText("Жанры:")
            self.age_films.setText("Возраст:")
            self.date_films.setText("Релиз:")
            self.description.setText("Описание:")

            self.name_film.setText("Фильм")

            self.label.setText("Фильмы")
        else:
            self.btn_clear_trailers.setText("Delete trailers")
            self.btn_clear_film_images.setText("Clear images")
            self.btn_exit_films.setText("<- back")

            self.btn_date_output.setText("By date")
            self.btn_name_output.setText("By name")
            self.btn_rating_output.setText("By rating")

            self.input_search_films.setText("Search...")

            self.pushButton.setText("Download the trailer")
            self.label_2.setText("Volume")

            self.rating_films.setText("Rating:")
            self.nation_films.setText("A country:")
            self.style_films.setText("Genre:")
            self.age_films.setText("Age:")
            self.date_films.setText("Release:")
            self.description.setText("Description")

            self.name_film.setText("Film")

            self.label.setText("Films")

    def clear_trailers_confirmation(self):
        """Функция потверждение трейлеров """

        if settings.get_confirmation() == "Вкл":
            valid = QMessageBox.question(self,
                                         'Подтверждение',
                                         'Вы точно хотите удалить трейлеры?\n'
                                         '(Функцию потверждения можно убрать в настройках)',
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                self.clear_trailers()
        else:
            self.clear_trailers()

    def clear_trailers(self):
        """Функция удаляет установлинные трейлеры"""
        directory_videos = listdir("data_videos/")
        data_on_downloaded_videos = set(
            filter(lambda p: p.endswith('.mp4') and p.startswith("F"), directory_videos)
        )

        for trailer in data_on_downloaded_videos:
            try:
                remove(f"data_videos/{trailer}")
            except PermissionError:
                QMessageBox.warning(self, "Информация",
                                    "Трейлер нельзя удалить изи за того что занят другим процессом\n"
                                    "Для решение проблемы выдете с приложения и зайдите")

    def download_trailer(self):
        """Загрузка трейлера"""

        # TODO: Попробовать реализовать полноэкранный экран

        directory_videos = listdir("data_videos/")
        data_on_downloaded_videos = set(
            filter(lambda p: p.endswith('.mp4') and p.startswith("F"), directory_videos)
        )

        filename = ''
        url_film_trailer = ''

        for value in sql.execute(f"SELECT video, id FROM data_films WHERE film = '{self.name_film_global}'"):

            filename = "F" + str(value[1])
            url_film_trailer = value[0]

        if self.name_film_global == '':
            QMessageBox.warning(self, "Информация", "Вам нужно выбрать фильм")

        elif filename + '.mp4' in data_on_downloaded_videos:

            """выводит трейлер с папки скаченных трейлеров на экран пользователю"""

            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"data_videos/{filename + '.mp4'}")))
            self.pushButton_2.setEnabled(True)
            self.ready_for_viewing.setText("Трейлер готов к запуску")

        else:

            if settings.get_confirmation() == "Вкл":

                valid = QMessageBox.question(self,
                                             'Подтверждение',
                                             'Трейлер не скачен, нужно будет немного подождать',
                                             QMessageBox.Yes, QMessageBox.No)

                if valid == QMessageBox.Yes:

                    """выводит трейлер с интернета на экран пользователю"""

                    self.download_trailer_yt(url_film_trailer, filename)
                else:
                    self.ready_for_viewing.setText("Трейлер не скачен")
            else:
                self.download_trailer_yt(url_film_trailer, filename)

    def download_trailer_yt(self, url, filename):

        """Скачивает и выводит на экран трейлер"""
        try:
            yt = YouTube(url)
            yt = yt.streams.filter(progressive=True, file_extension='').order_by('resolution').desc().first()
            yt.download("data_videos", filename + '.mp4')

            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"data_videos/{filename + '.mp4'}")))
            self.pushButton_2.setEnabled(True)
            self.ready_for_viewing.setText("Трейлер готов к запуску")
        except TypeError:
            QMessageBox.warning(self, "Информация", "Извените при попытке найти трейлер произошла ошибка")
        except pytube.exceptions.RegexMatchError:
            QMessageBox.warning(self, "Информация", "Извените при попытке найти трейлер произошла ошибка")

    def play(self):

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def media_state_changed(self):
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

    def set_volume(self):
        value = self.horizontalSlider_2.value()
        self.mediaPlayer.setVolume(value)
        self.statusbar.showMessage("Громкость " + str(value) + " %")

    # ------------------------<Дополнительные функции /* Для удобства работы с текстом *\>------------------------------

    def order_output_from_the_database(self):

        """Заголовок в котором показан порядок вывода информации"""

        self.table_films.addItem('№. film, [rating], nation, (release), style, age')

    def sort(self, state):

        """Добавление и удалений из множества категорий так же сразу осуществляется сортировка"""

        if state:
            self.data_criteria.add(self.sender().text().lower())
        else:
            self.data_criteria.remove(self.sender().text().lower())

        self.search_by_criteria()

    def creating_request(self):

        """
        создания запроса в БД

        Входные данные : Множество жанров -> {"Фантастика", "Ужасы"}
        Возращает запрос в базу данных -> ("Фантастика", "Ужасы")
        """

        return f'''('{"', '".join(self.data_criteria)}')'''

    def add_item(self, value, count):

        """Вывод фильмов и краткой инфмормации в таблицу"""

        self.table_films.addItem(f'{count}. '
                                 f'{value[0]}, '
                                 f'{value[1]}, '
                                 f'[{value[2]}], '
                                 f'({value[3]}), '
                                 f'{value[4]}+')

    def checking_search(self):

        """

        Функция дял проверки запроса на поиск ->
        Если фильм не найден то фукция убирает все и пишет "Фильм не найден".
        Если найден фильм то выводтся подробная информация.

        """

        # TODO: Улучишь поиск чтобы он мог искать не только по названию, но и по главным ролям. ->
        #  Если будет сделано то нужно не забыть выводить главных герояв в подробной информаци
        #  !!!ВАЖНО!!! Должно происходить автоматически (Тест функция возможно не попадет в релиз)

        # TODO: Улучьшить поиск (удаляел знаки, сделать поиск более удобным и точным)
        #  Примеры ошибок: Властелин колец возражение короля -> ничего не выведит потому что в бд
        #  Властелин колец: возражение короля
        #  Изменить данные в бд и в поиске удалять все не нужно (Будет доработана в будущем)

        input_search_data = self.input_search_films.text().strip().capitalize()

        verification_film = sql.execute(f"SELECT film FROM data_films WHERE film = '{input_search_data}'").fetchone()

        if verification_film is None:
            self.image_films.setText("Фильм не найден....")
            self.table_description_films.clear()
            self.output_rating_films.setText('')
            self.output_age_films.setText('')
            self.output_date_films.setText('')
            self.output_nation_films.setText('')
            self.output_style_films.setText('')
            self.name_film.setText('')
            self.output_reg.setText('')
            self.table_description_films.appendPlainText('')
            self.name_film_global = ''
        else:
            self.information_output(verification_film[0])

    def search_in_database(self, sorting, type_sorting):

        """Функция для поиска данных в базе данных и вывода в таблицу"""

        self.table_films.clear()
        self.order_output_from_the_database()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                     SELECT data_films.film, 
                            data_films.rating,
                            data_films.release, 
                            id_genres.genre, 
                            data_films.age
                     FROM data_films 
                            LEFT JOIN id_nations ON data_films.nation = id_nations.id 
                            LEFT JOIN id_genres ON data_films.genre = id_genres.id 
                     WHERE id_genres.genre in {self.creating_request()}
                     ORDER BY {sorting} {type_sorting}""").fetchall():
                self.add_item(value, count)
                count += 1
        else:
            for value in sql.execute(f"""
                     SELECT data_films.film, 
                            data_films.rating,
                            data_films.release, 
                            id_genres.genre, 
                            data_films.age
                     FROM data_films 
                            LEFT JOIN id_nations ON data_films.nation = id_nations.id 
                            LEFT JOIN id_genres ON data_films.genre = id_genres.id 
                     ORDER BY {sorting} {type_sorting}""").fetchall():
                self.add_item(value, count)
                count += 1

    # --------------------------------<Функции для вывода подробной информации фильма>----------------------------------

    def movie_selection(self):

        """Получаем выбранный фильм и редактируем под запрос"""

        selected_movie = self.table_films.currentItem().text()[3:].split(", ")
        if selected_movie[0] != 'film':
            self.information_output(selected_movie[0].strip())

    def information_output(self, film):

        """Функция для подробной информации по выбранному фильму"""

        self.table_description_films.clear()
        self.ready_for_viewing.setText(" ")
        self.name_film_global = film

        for value in sql.execute(f""" 
                     SELECT 
                            data_films.id,
                            data_films.film, 
                            data_films.rating, 
                            id_nations.nation, 
                            data_films.release, 
                            id_genres.genre, 
                            data_films.age, 
                            id_regisseurs.regisseur,
                            data_films.description,
                            data_films.image
                     FROM data_films 
                            LEFT JOIN id_nations ON data_films.nation = id_nations.id 
                            LEFT JOIN id_genres ON data_films.genre = id_genres.id 
                            LEFT JOIN id_regisseurs ON data_films.regisseur = id_regisseurs.id
                     WHERE data_films.film = '{film}'"""):

            # Изображение
            self.downloading_image(value[9], value[0])

            # Остальная информация

            self.output_rating_films.setText(f'{value[2]}')
            self.output_age_films.setText(f'{value[6]}+')
            self.output_reg.setText(f"{value[7]}")
            self.output_date_films.setText(f'{value[4]}')
            self.output_nation_films.setText(f'{value[3]}')
            self.output_style_films.setText(f'{value[5]}')
            self.name_film.setText(f'{value[1]}')
            self.table_description_films.appendPlainText(f'{value[8]}')

    def clear_images_confirmation(self):

        """Подтверждение на удаление"""

        if settings.get_confirmation() == "Вкл":
            valid = QMessageBox.question(self,
                                         'Подтверждение',
                                         'Вы точно хотите удалить изображения?\n'
                                         '(Функцию потверждение можно убрать в нстройках)',
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                self.clear_images()
        else:
            self.clear_images()

    @staticmethod
    def clear_images():

        """Функция удаляет изображения"""

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(
            filter(lambda p: p.endswith('.png') and p.startswith("F"), directory_images)
        )
        for image in data_on_downloaded_images:
            remove(f"data_images/{image}")

    def downloading_image(self, url, id_film):

        """
        Фунцкия для скачивания изображения с интернета и так же она сохраняет изображение с интернета
        на компьютере пользователя
        """

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(
            filter(lambda p: p.endswith('.png') and p.startswith("F"), directory_images)
        )

        id_film = "F" + str(id_film)

        if id_film + ".png" in data_on_downloaded_images:
            pixmap = QPixmap(f"data_images/{id_film}.png")
            self.image_films.setPixmap(pixmap)
        else:
            try:
                data = urllib.request.urlopen(url).read()

                f = open(f"data_images/{id_film}.png", "wb")
                f.write(data)
                f.close()

                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.image_films.setPixmap(pixmap)
            except AttributeError:
                pixmap = QPixmap("Noimage.jpg")
                self.image_films.setPixmap(pixmap)
            except ValueError:
                pixmap = QPixmap("Noimage.jpg")
                self.image_films.setPixmap(pixmap)
            except urllib.error.HTTPError:
                pixmap = QPixmap("Noimage.jpg")
                self.image_films.setPixmap(pixmap)
            except urllib.error.URLError:
                pixmap = QPixmap("Noimage.jpg")
                self.image_films.setPixmap(pixmap)

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

    def basic_by_output(self):

        """Базовый вывод"""

        self.search_in_database("rating", "DESC")

    def output_by_rating(self):

        """Вывод фильмов по рейтингу"""

        self.search_in_database("rating", "DESC")

    def output_by_date(self):

        """Вывод фильмов по дате релиза"""

        self.search_in_database("release", "DESC")

    def output_by_name(self):

        """Вывод фильмов по названию"""

        self.search_in_database("film", "ASC")

    def search_by_criteria(self):

        """Сортировка по критериям"""

        self.search_in_database("rating", "DESC")

    #  -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _exit():
        films.close()
        ex.show()

    def closeEvent(self, event):

        self.mediaPlayer.pause()
        self.basic_by_output()


class Serials(QMainWindow, Serials_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.name_serials_global = ''

        self.data_criteria = set()

        self.setWindowIcon(QIcon('icon.png'))

        self.basic_by_output()

        # ---------------------------------------------<Кнопки и интерфейс>---------------------------------------------

        self.data_criteria_serials = set()

        # Критерии

        self.checkBox.clicked.connect(self.sort)
        self.checkBox_2.clicked.connect(self.sort)
        self.checkBox_3.clicked.connect(self.sort)
        self.checkBox_4.clicked.connect(self.sort)
        self.checkBox_5.clicked.connect(self.sort)
        self.checkBox_6.clicked.connect(self.sort)
        self.checkBox_7.clicked.connect(self.sort)
        self.checkBox_8.clicked.connect(self.sort)
        self.checkBox_9.clicked.connect(self.sort)

        # Кнопки

        self.btn_exit_serials.clicked.connect(self._exit)
        self.btn_clear_serials_images.clicked.connect(self.clear_images_confirmation)
        self.btn_clear_trailers.clicked.connect(self.clear_trailers_confirmation)

        # Кнопки Основных критерий

        self.btn_date_DESC_serials.clicked.connect(self.output_by_date)
        self.btn_name_DESC_serials.clicked.connect(self.output_by_name)
        self.btn_rating_DESC_serials.clicked.connect(self.output_by_rating)

        # Кнопка нужна для вывода подробной информации -> При нажатии на фильм будет выведина полная информация
        self.table_serials.clicked.connect(self.movie_selection)

        # Нажатие Поиска на Enter
        self.input_search_serials.returnPressed.connect(self.checking_search)

        #

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.mediaPlayer.stateChanged.connect(self.media_state_changed)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
        self.horizontalSlider_2.sliderMoved.connect(self.set_volume)

        self.mediaPlayer.setVideoOutput(self.widget_film_trailer)
        self.pushButton.clicked.connect(self.download_trailer)
        self.pushButton_2.clicked.connect(self.play)

        self.mediaPlayer.setVolume(50)

        self.table_serials.clicked.connect(self.movie_selection)

    # ------------------------<Дополнительные функции /* Для удобства работы с текстом *\>------------------------------
    def clear_trailers_confirmation(self):
        """Функция потверждение трейлеров """

        if settings.get_confirmation() == "Вкл":
            valid = QMessageBox.question(self,
                                         'Подтверждение',
                                         'Вы точно хотите удалить трейлеры?\n'
                                         '(Функцию потверждения можно убрать в настройках)',
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                self.clear_trailers()
        else:
            self.clear_trailers()

    def clear_trailers(self):
        """Функция удаляет установлинные трейлеры"""
        directory_videos = listdir("data_videos/")
        data_on_downloaded_videos = set(
            filter(lambda p: p.endswith('.mp4') and p.startswith("S"), directory_videos)
        )

        for trailer in data_on_downloaded_videos:
            try:
                remove(f"data_videos/{trailer}")
            except PermissionError:
                QMessageBox.warning(self, "Информация", "не можем удалить трейлер трейлер открыт другим процессом\n"
                                    "Для решение проблемы выдете с приложения и зайдите")

    def download_trailer(self):
        """Загрузка трейлера"""

        # TODO: Попробовать реализовать полноэкранный экран (будет реализованно в будущим)

        directory_videos = listdir("data_videos/")
        data_on_downloaded_videos = set(
            filter(lambda p: p.endswith('.mp4') and p.startswith("S"), directory_videos)
        )

        filename = ''
        url_serials_trailer = ''

        for value in sql.execute(f"SELECT videos, id FROM data_serials WHERE serial = '{self.name_serials_global}'"):
            filename = "S" + str(value[1])
            url_serials_trailer = value[0]

        if self.name_serials_global == '':
            QMessageBox.warning(self, "Информация", "Вам нужно выбрать фильм")

        elif filename + '.mp4' in data_on_downloaded_videos:

            """выводит трейлер с папки скаченных трейлеров на экран пользователю"""

            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"data_videos/{filename + '.mp4'}")))
            self.pushButton_2.setEnabled(True)
            self.ready_for_viewing.setText("Трейлер готов к запуску")

        else:

            if settings.get_confirmation() == "Вкл":

                valid = QMessageBox.question(self,
                                             'Подтверждение',
                                             'Трейлер не скачен, нужно будет немного подождать',
                                             QMessageBox.Yes, QMessageBox.No)

                if valid == QMessageBox.Yes:

                    """выводит трейлер с интернета на экран пользователю"""

                    self.download_trailer_yt(url_serials_trailer, filename)
                else:
                    self.ready_for_viewing.setText("Трейлер не скачен")
            else:
                self.download_trailer_yt(url_serials_trailer, filename)

    def download_trailer_yt(self, url, filename):

        """Скачивает и выводит на экран трейлер"""

        # Помогает сократить код
        try:
            yt = YouTube(url)
            yt = yt.streams.filter(progressive=True, file_extension='').order_by('resolution').desc().first()
            yt.download("data_videos", filename + '.mp4')

            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f"data_videos/{filename + '.mp4'}")))
            self.pushButton_2.setEnabled(True)
            self.ready_for_viewing.setText("Трейлер готов к запуску")
        except pytube.exceptions.RegexMatchError:
            QMessageBox.warning(self, "Информация", "Извените при попытке найти трейлер произошла ошибка")

    def play(self):

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def media_state_changed(self):
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

    def set_volume(self):
        value = self.horizontalSlider_2.value()
        self.mediaPlayer.setVolume(value)
        self.statusbar.showMessage("Громкость " + str(value) + " %")

    # ------------------------<Дополнительные функции /* Для удобства работы с текстом *\>------------------------------

    def order_output_from_the_database(self):

        """Заголовок в котором показан порядок вывода информации"""

        self.table_serials.addItem('№. serial, [rating], nation, (release), style, age')

    def sort(self, state):

        """Добавление и удалений из множества категорий так же сразу осуществляется сортировка"""

        if state:
            self.data_criteria.add(self.sender().text().lower())
        else:
            self.data_criteria.remove(self.sender().text().lower())

        self.search_by_criteria()

    def creating_request(self):

        """
        создания запроса в БД

        Входные данные : Множество жанров -> {"Фантастика", "Ужасы"}
        Возращает запрос в базу данных -> ("Фантастика", "Ужасы")
        """

        return f'''('{"', '".join(self.data_criteria)}')'''

    def add_item(self, value, count):

        """Вывод фильмов и краткой инфмормации в таблицу"""

        self.table_serials.addItem(f'{count}. '
                                   f'{value[0]}, '
                                   f'{value[1]}, '
                                   f'[{value[2]}], '
                                   f'({value[3]}), '
                                   f'{value[4]}+, '
                                   f'{value[5]}')

    def checking_search(self):

        """

        Функция дял проверки запроса на поиск ->
        Если фильм не найден то фукция убирает все и пишет "Фильм не найден".
        Если найден фильм то выводтся подробная информация.

        """

        # TODO: Улучишь поиск чтобы он мог искать не только по названию, но и по главным ролям. ->
        #  Если будет сделано то нужно не забыть выводить главных герояв в подробной информаци
        #  !!!ВАЖНО!!! Должно происходить автоматически (Тест функция возможно не попадет в релиз)

        # TODO: улучьшить поиск
        input_search_data = self.input_search_serials.text().strip().capitalize()

        verification_serials = \
            sql.execute(f'SELECT serial FROM data_serials WHERE serial = "{input_search_data}"').fetchone()

        if verification_serials is None:
            self.image_serials.setText("Фильм не найден....")
            self.table_description_serials.clear()
            self.output_rating_films.setText('')
            self.output_age_films.setText('')
            self.output_date_films.setText('')
            self.output_seasons_films.setText('')
            self.output_nation_films.setText('')
            self.output_style_films.setText('')
            self.output_reg.setText("")
            self.name_film.setText('')

        else:
            self.information_output(verification_serials[0])

    def search_in_database(self, sorting, type_sorting):

        """Функция для поиска данных в базе данных и вывода в таблицу"""

        self.table_serials.clear()
        self.order_output_from_the_database()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                     SELECT data_serials.serial, 
                            data_serials.rating, 
                            data_serials.release, 
                            id_genres.genre, 
                            data_serials.age, 
                            data_serials.seasons
                     FROM data_serials 
                            LEFT JOIN id_nations ON data_serials.nation = id_nations.id 
                            LEFT JOIN id_genres ON data_serials.genre = id_genres.id 
                     WHERE id_genres.genre in {self.creating_request()}
                     ORDER BY {sorting} {type_sorting}"""):
                self.add_item(value, count)
                count += 1
        else:
            for value in sql.execute(f"""
                     SELECT data_serials.serial, 
                            data_serials.rating, 
                            data_serials.release, 
                            id_genres.genre, 
                            data_serials.age, 
                            data_serials.seasons
                     FROM data_serials 
                            LEFT JOIN id_nations ON data_serials.nation = id_nations.id 
                            LEFT JOIN id_genres ON data_serials.genre = id_genres.id 
                     ORDER BY {sorting} {type_sorting}"""):
                self.add_item(value, count)
                count += 1

    # --------------------------------<Функции для вывода подробной информации фильма>----------------------------------

    def movie_selection(self):

        """Получаем выбранный фильм и редактируем под запрос"""

        selected_serial = self.table_serials.currentItem().text()[3:].split(", ")
        if selected_serial[0] != 'serial':
            self.information_output(selected_serial[0].strip())

    def information_output(self, serials):

        """Функция для подробной информации по выбранному фильму"""

        self.table_description_serials.clear()
        self.ready_for_viewing.setText(" ")
        self.name_serials_global = serials

        for value in sql.execute(f"""
                     SELECT data_serials.id,
                            data_serials.serial, 
                            data_serials.rating,
                            id_nations.nation,
                            data_serials.release, 
                            id_genres.genre, 
                            data_serials.age,
                            data_serials.description,
                            id_regisseurs.regisseur,
                            data_serials.seasons,
                            data_serials.images
                     FROM data_serials 
                            LEFT JOIN id_nations ON data_serials.nation = id_nations.id 
                            LEFT JOIN id_genres ON data_serials.genre = id_genres.id  
                            LEFT JOIN id_regisseurs ON data_serials.regisseur = id_regisseurs.id
                     WHERE serial = '{serials}'"""):
            # Изображение
            self.downloading_image(value[10], value[0])

            # Остальная информация
            self.output_rating_films.setText(f'{value[2]}')
            self.output_age_films.setText(f'{value[6]}+')
            self.output_date_films.setText(f'{value[4]}')
            self.output_seasons_films.setText(f'{value[9]}')
            self.output_nation_films.setText(f'{value[3]}')
            self.output_style_films.setText(f'{value[5]}')
            self.output_reg.setText(f"{value[8]}")
            self.name_film.setText(f'{value[1]}')
            self.table_description_serials.appendPlainText(f'{value[7]}')

    def clear_images_confirmation(self):

        """Подтверждение на удаление"""

        if settings.get_confirmation() == "Вкл":
            valid = QMessageBox.question(self,
                                         'Подтверждение',
                                         'Вы точно хотите удалить изображения?\n'
                                         '(Функцию потверждение можно убрать в нстройках)',
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                self.clear_images()
        else:
            self.clear_images()

    @staticmethod
    def clear_images():

        """Функция удаляет изображения"""

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(
            filter(lambda p: p.endswith('.png') and p.startswith("S"), directory_images)
        )

        for image in data_on_downloaded_images:
            remove(f"data_images/{image}")

    def downloading_image(self, url, id_film):

        """
        Фунцкия для скачивания изображения с интернета и так же она сохраняет изображение с интернета
        на компьютере пользователя
        """

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(
            filter(lambda p: p.endswith('.png') and p.startswith("S"), directory_images)
        )
        id_film = "S" + str(id_film)

        if id_film + ".png" in data_on_downloaded_images:

            pixmap = QPixmap(f"data_images/{id_film}.png")
            self.image_serials.setPixmap(pixmap)
        else:
            try:
                data = urllib.request.urlopen(url).read()

                f = open(f"data_images/{id_film}.png", "wb")
                f.write(data)
                f.close()
                pixmap = QPixmap(f"data_images/{id_film}.png")
                self.image_serials.setPixmap(pixmap)

            except AttributeError:
                pixmap = QPixmap("Noimage.jpg")
                self.image_serials.setPixmap(pixmap)

            except ValueError:
                pixmap = QPixmap("Noimage.jpg")
                self.image_serials.setPixmap(pixmap)

            except urllib.error.HTTPError:
                pixmap = QPixmap("Noimage.jpg")
                self.image_serials.setPixmap(pixmap)

            except urllib.error.URLError:
                pixmap = QPixmap("Noimage.jpg")
                self.image_serials.setPixmap(pixmap)

    # ----------------------------------------------<Основные Критерии>-------------------------------------------------

    def basic_by_output(self):

        """Базовый вывод"""

        self.search_in_database("rating", "DESC")

    def output_by_rating(self):

        """Вывод фильмов по рейтингу"""

        self.search_in_database("rating", "DESC")

    def output_by_date(self):

        """Вывод фильмов по дате релиза"""

        self.search_in_database("release", "DESC")

    def output_by_name(self):

        """Вывод фильмов по названию"""

        self.search_in_database("serial", "ASC")

    def search_by_criteria(self):

        """Сортировка по критериям"""

        self.search_in_database("rating", "DESC")

    #  -----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _exit():
        serial.close()
        ex.show()

    def closeEvent(self, event):

        self.mediaPlayer.pause()
        self.basic_by_output()


class BooksComics(QMainWindow, Books_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowIcon(QIcon('icon.png'))

        self.data_criteria = set()

        self.basic_by_output()

        # Все критерии -> Вывод фильмов по критериям

        self.checkBox_12.clicked.connect(self.sort)
        self.checkBox_11.clicked.connect(self.sort)
        self.checkBox_10.clicked.connect(self.sort)
        self.checkBox_9.clicked.connect(self.sort)
        self.checkBox_8.clicked.connect(self.sort)
        self.checkBox_7.clicked.connect(self.sort)
        self.checkBox_6.clicked.connect(self.sort)
        self.checkBox.clicked.connect(self.sort)

        # Кнопки Основных критерий

        self.table_books.clicked.connect(self.movie_selection)

        self.input_search.returnPressed.connect(self.checking_search)

        self.btn_clear_images.clicked.connect(self.clear_images_confirmation)
        self.btn_date_DESC.clicked.connect(self.output_by_date)
        self.btn_name_DESC.clicked.connect(self.output_by_name)

        self.btn_exit.clicked.connect(self.exit)

    def gui(self):
        """нужна дял смены языка"""
        # TODO: реальзвоать смену интерфейса
        pass

    def clear_images_confirmation(self):

        """Подтверждение на удаление"""

        if settings.get_confirmation() == "Вкл":
            valid = QMessageBox.question(self,
                                         'Подтверждение',
                                         'Вы точно хотите удалить изображения?\n'
                                         '(Функцию потверждение можно убрать в нстройках)',
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                self.clear_images()
        else:
            self.clear_images()

    @staticmethod
    def clear_images():

        """Функция удаляет изображения"""

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(
            filter(lambda p: p.endswith('.png') and p.startswith("B"), directory_images)
        )
        for image in data_on_downloaded_images:
            remove(f"data_images/{image}")

    def downloading_image(self, url, id_book):
        """
        Фунцкия для скачивания изображения с интернета и так же она сохраняет изображение с интернета
        на компьютере пользователя
        """

        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(
            filter(lambda p: p.endswith('.png') and p.startswith("B"), directory_images)
        )

        id_book = "B" + str(id_book)

        if id_book + ".png" in data_on_downloaded_images:
            pixmap = QPixmap(f"data_images/{id_book}.png")
            self.image.setPixmap(pixmap)
        else:
            try:
                data = urllib.request.urlopen(url).read()

                f = open(f"data_images/{id_book}.png", "wb")
                f.write(data)
                f.close()

                pixmap = QPixmap()
                pixmap.loadFromData(data)
                self.image.setPixmap(pixmap)
            except AttributeError:
                pixmap = QPixmap("Noimage.jpg")
                self.image.setPixmap(pixmap)

            except ValueError:
                pixmap = QPixmap("Noimage.jpg")
                self.image.setPixmap(pixmap)

            except urllib.error.HTTPError:
                pixmap = QPixmap("Noimage.jpg")
                self.image.setPixmap(pixmap)

            except urllib.error.URLError:
                pixmap = QPixmap("Noimage.jpg")
                self.image.setPixmap(pixmap)

    @staticmethod
    def isint(verification_number):

        try:
            int(verification_number)
            return True
        except ValueError:
            return False

    def checking_search(self):
        """

        Функция дял проверки запроса на поиск ->
        Если книга не найден то фукция убирает все и пишет "книга не найден".
        Если найдена книга то выводтся подробная информация.

        """
        input_search_data = self.input_search.text().strip().split()

        if self.isint(input_search_data[-1]):
            book = " ".join(input_search_data[:len(input_search_data) - 1]).capitalize()
            tom = input_search_data[-1]
        else:
            book = " ".join(input_search_data).capitalize()
            tom = 1

        verification_film = sql.execute(f'SELECT book, toms FROM data_books WHERE book = "{book}" and toms = {tom}'
                                        ).fetchmany(2)
        if len(verification_film) < 1:
            self.image.setText("Книга не найдена....")
            self.table_description.clear()
            self.output_date.setText('')
            self.output_style.setText('')
            self.output_author.setText("")
            self.name.setText('')
            self.output_tom.setText("")
            self.table_description.appendPlainText('')
        else:
            self.information_output(verification_film[0][0], verification_film[0][1])

    def movie_selection(self):

        """Получаем выбранный фильм и редактируем под запрос"""

        selected_movie = self.table_books.currentItem().text()[3:].strip().split(", ")
        if selected_movie[0] != 'book':
            self.information_output(selected_movie[0].strip(), selected_movie[4].strip())

    def information_output(self, book, tom):

        """Функция для подробной информации по выбранному фильму"""

        self.table_description.clear()

        for value in sql.execute(f"""
                     SELECT 
                            data_books.id,
                            data_books.book, 
                            data_books.release, 
                            id_authors.author, 
                            id_genres_books.genre, 
                            data_books.toms,
                            data_books.discraption,
                            data_books.image
                     FROM data_books 
                            LEFT JOIN id_authors ON data_books.author = id_authors.id 
                            LEFT JOIN id_genres_books ON data_books.genre = id_genres_books.id  
                     WHERE book = '{book}' and toms = {tom}"""):
            # Изображение
            self.downloading_image(value[7], value[0])

            self.output_author.setText(f'{value[3]}')
            self.output_date.setText(f'{value[2]}')
            self.output_style.setText(f'{value[4]}')
            self.output_tom.setText(f'{value[5]}')
            self.name.setText(f'{value[1]}')
            self.table_description.appendPlainText(f'{value[6]}')

    def creating_request(self):

        """
            создания запроса в БД

            Входные данные : Множество жанров -> {"Фантастика", "Ужасы"}
            Возращает запрос в базу данных -> ("Фантастика", "Ужасы")
        """

        return f'''('{"', '".join(self.data_criteria)}')'''

    def sort(self, state):

        """Добавление и удалений из множества категорий так же сразу осуществляется сортировка"""

        if state:
            self.data_criteria.add(self.sender().text().lower())
        else:
            self.data_criteria.remove(self.sender().text().lower())

        self.output_by_sort_criteria()

    def add_item(self, value, count):

        """Вывод фильмов и краткой инфмормации в таблицу"""

        self.table_books.addItem(f'{count}. '
                                 f'{value[0]}, '
                                 f'{value[1]}, '
                                 f'{value[2]}, '
                                 f'{value[3]}, '
                                 f'{value[4]}')

    def order_output_from_the_database(self):

        """Заголовок в котором показан порядок вывода информации"""

        self.table_books.addItem("book, release, author, genre, tom")

    def search_in_database(self, sorting, type_sorting):

        """Функция для поиска данных в базе данных и вывода в таблицу"""

        self.table_books.clear()
        self.order_output_from_the_database()
        count = 1
        if len(self.data_criteria) > 0:
            for value in sql.execute(f"""
                     SELECT data_books.book, 
                            data_books.release, 
                            id_authors.author, 
                            id_genres_books.genre, 
                            data_books.toms  
                     FROM data_books 
                            LEFT JOIN id_authors ON data_books.author = id_authors.id 
                            LEFT JOIN id_genres_books ON data_books.genre = id_genres_books.id 
                     WHERE id_genres_books.genre in {self.creating_request()}
                     ORDER BY {sorting} {type_sorting}""").fetchall():
                self.add_item(value, count)
                count += 1
        else:
            for value in sql.execute(f"""
                     SELECT data_books.book, 
                            data_books.release, 
                            id_authors.author, 
                            id_genres_books.genre, 
                            data_books.toms  
                     FROM data_books 
                            LEFT JOIN id_authors ON data_books.author = id_authors.id 
                            LEFT JOIN id_genres_books ON data_books.genre = id_genres_books.id 
                     ORDER BY {sorting} {type_sorting}""").fetchall():
                self.add_item(value, count)
                count += 1

    def basic_by_output(self):

        """Базовый вывод"""

        self.search_in_database("release", "DESC")

    def output_by_date(self):

        """Вывод книг по дате"""

        self.search_in_database("release", "DESC")

    def output_by_name(self):

        """вывод книг по названию"""

        self.search_in_database("book", "ASC")

    def output_by_sort_criteria(self):

        """Вывод книги по нажатию на жанр"""

        self.search_in_database("release", "DESC")

    @staticmethod
    def exit():
        books_and_comics.close()
        ex.show()


class Settings(QMainWindow, Settings_ui):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.add_confirmation_item()
        self.add_language_item()

        self.btn_exit.clicked.connect(self.exit)
        self.confirmation.currentTextChanged.connect(self.set_confirmation)
        self.language.currentTextChanged.connect(self.set_language)
        self.btn_clear_all_images.clicked.connect(self.clear_all_images_confirmation)
        self.btn_clear_all_trailers.clicked.connect(self.clear_all_trailers_confirmation)

    def clear_all_images_confirmation(self):

        if self.get_confirmation() == "Выкл":
            self.clear_all_images()
        else:
            valid = QMessageBox.question(self,
                                         'Подтверждение',
                                         'Вы точно хотите удалить все изображения?\n'
                                         '(Функцию потверждения можно выключить в настройках)',
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                self.clear_all_images()

    def clear_all_trailers_confirmation(self):

        if self.get_confirmation() == "Выкл":
            self.clear_all_trailers()
        else:
            valid = QMessageBox.question(self,
                                         'Подтверждение',
                                         'Вы точно хотите удалить все трейлеры?\n'
                                         '(Функцию потверждения можно выключить в настройках)',
                                         QMessageBox.Yes, QMessageBox.No)

            if valid == QMessageBox.Yes:
                self.clear_all_trailers()

    @staticmethod
    def clear_all_images():
        directory_images = listdir("data_images/")
        data_on_downloaded_images = set(
            filter(lambda p: p.endswith('.png'), directory_images)
        )

        if len(data_on_downloaded_images) > 0:
            for image in data_on_downloaded_images:
                remove(f"data_images/{image}")

    def clear_all_trailers(self):
        directory_videos = listdir("data_videos/")
        data_on_downloaded_videos = set(
            filter(lambda p: p.endswith(".mp4"), directory_videos)
        )

        if len(data_on_downloaded_videos) > 0:
            for video in data_on_downloaded_videos:
                try:
                    remove(f"data_videos/{video}")
                except PermissionError:
                    QMessageBox.warning(self, "Информация", "не можем удалить трейлер трейлер открыт другим процессом\n"
                                                            "Для решение проблемы выдете с приложения и зайдите")

    def add_confirmation_item(self):
        if sql.execute("SELECT confirmation FROM user").fetchone()[0] == "Вкл":
            self.confirmation.addItem("Вкл")
            self.confirmation.addItem("Выкл")
        else:
            self.confirmation.addItem("Выкл")
            self.confirmation.addItem("Вкл")

    def add_language_item(self):
        if sql.execute("SELECT language FROM user").fetchone()[0] == "Ru":
            self.language.addItem("Ru")
            self.language.addItem("Eng")
        else:
            self.language.addItem("Eng")
            self.language.addItem("Ru")

    @staticmethod
    def set_language(text):
        sql.execute(f"UPDATE user SET language = '{text}' WHERE id = 1")
        db.commit()

    @staticmethod
    def get_language():
        return sql.execute("SELECT language FROM user").fetchone()[0]

    @staticmethod
    def set_confirmation(text):
        sql.execute(f"UPDATE user SET confirmation = '{text}' WHERE id = 1")
        db.commit()

    @staticmethod
    def get_confirmation():
        return sql.execute("SELECT confirmation FROM user").fetchone()[0]

    @staticmethod
    def exit():
        settings.close()
        ex.show()


def except_hook(cls, exception, traceback):
    sys.excepthook(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
