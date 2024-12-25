from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QDialog
from Note import Note


# В данном файле прописан класс работы виджета для редактирования заметки

class EditNoteWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.number = None  # Данные о заметке
        self.title = None
        self.text = None
        self.type = None
        self.progress = None

        uic.loadUi('static/ui/EditNoteWidget.ui', self)  # Импорт ui файла

        self.green_button.clicked.connect(lambda: self.ChangeType(1))  # Назначение действий при нажатии на зелёную кнопку (кнопка меняет тип заметки (задачи))
        self.yellow_button.clicked.connect(lambda: self.ChangeType(2))  # Назначение действий при нажатии на жёлтую кнопку (кнопка меняет тип заметки (задачи))
        self.red_button.clicked.connect(lambda: self.ChangeType(3))  # Назначение действий при нажатии на красную кнопку (кнопка меняет тип заметки (задачи))
        self.progress_up_button.clicked.connect(
            lambda: self.ChangeProgress(4))  # Назначение действий при нажатии на кнопку повышения прогресса заметки
        self.progress_down_button.clicked.connect(
            lambda: self.ChangeProgress(-4))  # Назначение действий при нажатии на кнопку понижения прогресса заметки

    def CreateWindow(self, number, note):  # Метод для отображения окна
        self.number = number  # Получение номера заметки
        self.title = note.title  # Получение оглавления заметки
        self.title_field.setText(self.title)  # Размещение оглавления заметки на поле для редактирования

        self.text = note.text  # Получение текста заметки
        self.text_field.setText(self.text)  # Размещение текста заметки на поле для редактирования

        self.type = note.type  # Получение типа заметки
        self.progress = note.progress  # Получение прогресса заметки

        if self.type == 'Job_is_done':  # Включение
            self.type = ''  # и выключение
            self.ChangeType(1)  # нужных кнопок
        elif self.type == 'Job_in_progress':  # в зависимости от
            self.type = ''  # типа
            self.ChangeType(2)  # заметки
        elif self.type == 'Job_is_cancelled':
            self.type = ''
            self.ChangeType(3)

        pixmap = self.GetProgressBarImage(self.type,
                                          self.progress)  # Получение изображение шкалы прогресса в зависимости от типа и прогресса заметки
        self.progress_bar.setPixmap(pixmap)  # Устанавливаем нужное изображение шкалы прогресса

        self.window().show()  # Показать текущее окно

    @staticmethod
    def GetProgressBarImage(note_type, progress):  # Метод для получения изображения шкалы прогресса в зависимости от типа и прогресса заметки
        progress_bar_pixmap = None
        if note_type == 'Job_is_done':
            progress_bar_pixmap = QPixmap('static/img/full_green.png')
        elif note_type == 'Job_in_progress':
            if progress < 10:
                progress_bar_pixmap = QPixmap('static/img/empty.png')
            elif 10 <= progress < 20:
                progress_bar_pixmap = QPixmap('static/img/10_yellow.png')
            elif 20 <= progress < 30:
                progress_bar_pixmap = QPixmap('static/img/20_yellow.png')
            elif 30 <= progress < 40:
                progress_bar_pixmap = QPixmap('static/img/30_yellow.png')
            elif 40 <= progress < 50:
                progress_bar_pixmap = QPixmap('static/img/40_yellow.png')
            elif 50 <= progress < 60:
                progress_bar_pixmap = QPixmap('static/img/50_yellow.png')
            elif 60 <= progress < 70:
                progress_bar_pixmap = QPixmap('static/img/60_yellow.png')
            elif 70 <= progress < 80:
                progress_bar_pixmap = QPixmap('static/img/70_yellow.png')
            elif 80 <= progress < 90:
                progress_bar_pixmap = QPixmap('static/img/80_yellow.png')
            elif 90 <= progress < 100:
                progress_bar_pixmap = QPixmap('static/img/90_yellow.png')
        elif note_type == 'Job_is_cancelled':
            if progress < 10:
                progress_bar_pixmap = QPixmap('static/img/empty.png')
            elif 10 <= progress < 20:
                progress_bar_pixmap = QPixmap('static/img/10_red.png')
            elif 20 <= progress < 30:
                progress_bar_pixmap = QPixmap('static/img/20_red.png')
            elif 30 <= progress < 40:
                progress_bar_pixmap = QPixmap('static/img/30_red.png')
            elif 40 <= progress < 50:
                progress_bar_pixmap = QPixmap('static/img/40_red.png')
            elif 50 <= progress < 60:
                progress_bar_pixmap = QPixmap('static/img/50_red.png')
            elif 60 <= progress < 70:
                progress_bar_pixmap = QPixmap('static/img/60_red.png')
            elif 70 <= progress < 80:
                progress_bar_pixmap = QPixmap('static/img/70_red.png')
            elif 80 <= progress < 90:
                progress_bar_pixmap = QPixmap('static/img/80_red.png')
            elif 90 <= progress < 100:
                progress_bar_pixmap = QPixmap('static/img/90_red.png')
        return progress_bar_pixmap

    def ChangeType(self, button_id):  # Метод для изменения типа заметки при нажатии на кнопку
        if button_id == 1 and self.type != 'Job_is_done':  # Если была нажата зелёная кнопка и тип заметки != Задача выполнена
            self.type = 'Job_is_done'  # Меняем тип заметки
            self.green_button.setIcon(QIcon('static/img/lump_green_on.png'))  # Меняем внешний
            self.yellow_button.setIcon(QIcon('static/img/lump_yellow_off.png'))  # вид кнопок
            self.red_button.setIcon(QIcon('static/img/lump_red_off.png'))  # смены типа заметки
            self.status_label.setText('Тип заметки(задачи):\nЗадача выполнена!')  # Меняем текст типа заметки
            self.progress_text.setText('')  # Меняем текст прогресса заметки
            self.progress_up_button.setEnabled(False)  # Делаем кнопки смены прогресса
            self.progress_down_button.setEnabled(False)  # недоступными для взаимодействия
        elif button_id == 2 and self.type != 'Job_in_progress':  # Если была нажата жёлтая кнопка и тип заметки != Задача выполняется
            self.type = 'Job_in_progress'  # Меняем тип заметки
            self.green_button.setIcon(QIcon('static/img/lump_green_off.png'))  # Меняем внешний
            self.yellow_button.setIcon(QIcon('static/img/lump_yellow_on.png'))  # вид кнопок
            self.red_button.setIcon(QIcon('static/img/lump_red_off.png'))  # смены типа заметки
            self.status_label.setText('Тип заметки(задачи):\nЗадача выполняется')  # Меняем текст типа заметки
            if self.progress == 100:  # Если прогресс = 100%, понижаем его до 96% (это надо, так как тип заметки
                self.progress = 96  # автоматически меняестя на 'Задача выполнена' при повышении прогресса до 100%)
            self.progress_text.setText(f'Прогресс: {self.progress}%')  # Меняем текст прогресса заметки
            self.progress_text.setStyleSheet('color: #fbfd53;border: none;')  # Меняем стиль текста прогресса заметки
            self.progress_up_button.setEnabled(True)  # Делаем кнопки смены прогресса
            self.progress_down_button.setEnabled(True)  # доступными для взаимодействия
        elif button_id == 3 and self.type != 'Job_is_cancelled':  # Если была нажата красная кнопка и тип заметки != Задача отложена
            self.type = 'Job_is_cancelled'  # Меняем тип заметки
            self.green_button.setIcon(QIcon('static/img/lump_green_off.png'))  # Меняем внешний
            self.yellow_button.setIcon(QIcon('static/img/lump_yellow_off.png'))  # вид кнопок
            self.red_button.setIcon(QIcon('static/img/lump_red_on.png'))  # смены типа заметки
            self.status_label.setText('Тип заметки(задачи):\nЗадача отложена')  # Меняем текст типа заметки
            if self.progress == 100:  # Если прогресс = 100%, понижаем его до 96% (это надо, так как тип заметки
                self.progress = 96  # автоматически меняестя на 'Задача выполнена' при повышении прогресса до 100%)
            self.progress_text.setText(f'Прогресс: {self.progress}%')  # Меняем текст прогресса заметки
            self.progress_text.setStyleSheet('color: #ff0000;border: none;')  # Меняем стиль текста прогресса заметки
            self.progress_up_button.setEnabled(False)  # Делаем кнопки смены прогресса
            self.progress_down_button.setEnabled(False)  # недоступными для взаимодействия
        pixmap = self.GetProgressBarImage(self.type, self.progress)  # Получение изображение шкалы прогресса в зависимости от типа и прогресса заметки
        self.progress_bar.setPixmap(pixmap)  # Устанавливаем нужное изображение шкалы прогресса

    def ChangeProgress(self, delta):  # Действия при нажатии на кнопки смены прогресса (delta - значение смены прогресса)
        if 0 <= self.progress + delta <= 100:  # Проверяем, будет ли находиться значение прогресса, если мы его изменим на delta
            self.progress += delta  # Если да, то меняем значение прогресса
        if self.progress == 100:  # Если прогресс достиг 100%
            self.ChangeType(1)  # Вызываем метод для смены типа заметки на 'Задача выполнена'
        else:
            pixmap = self.GetProgressBarImage(self.type, self.progress)  # Получение изображение шкалы прогресса в зависимости от типа и прогресса заметки
            self.progress_bar.setPixmap(pixmap)  # Устанавливаем нужное изображение шкалы прогресса
            self.progress_text.setText(f'Прогресс: {self.progress}%')  # Меняем текст прогресса заметки

    def CloseWindow(self):  # Метод для сокрытия окна
        self.window().hide()  # Спрятать текущее окно

    def GetUpdatedNote(self):  # Метод для получения данных отредактированной заметки (используется другими классами)
        note = Note(self.title_field.text(), self.text_field.toPlainText(), self.type, self.progress)  # Создание заметки из данных, находящихся на окне
        return note  # Возвращение заметки
