from PyQt5 import uic, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QGridLayout, QSizePolicy
from EditNoteWidget import EditNoteWidget
from Note import Note
from EditNameWidget import EditNameWidget

# В данном файле прописан класс работы главного окна приложения

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.user_data = None  # Данные
        self.user_id = None    # об
        self.name = None       # аккаун-
        self.notes = None      # те

        uic.loadUi('static/ui/MainWindow.ui', self)  # Импорт ui файла

        self.layout = QGridLayout(self.notes_board)  # Создание сетки на фрейме с заметками
        for i in range(4):
            self.layout.setColumnMinimumWidth(i, 400)  # Устанавливаем минимальную ширину в 400 пикселей для каждого столбца сетки
        self.layout.setSpacing(20)  # Устанавливаем расстояние в 20 пикселей между ячейками сетки
        self.add_button.clicked.connect(lambda: self.AddNote())  # Назначение действия при нажатии на кнопку добавления заметки
        self.edit_name_page = EditNameWidget()  # Создание экземпляра класса окна редактирования имени

    def CreateWindow(self, user_data):  # Метод для отображения окна
        self.user_data = user_data  # Получение данных аккаунта, переданных в метод
        self.user_id = user_data['id']  # Получение id ккаунта из данных аккаунта

        self.name = user_data['name']  # Получение имени пользователя из данных аккаунта
        self.SetTextName()  # Размещение имени на панели приветствия пользователя в правом верхнем углу экрана
        self.edit_name_page.name_input_field.setText(self.name) # Размещаем имя в поле для смены имени

        self.notes = user_data['notes']  # Получение списка заметок из данных аккаунта

        self.edit_name_button.clicked.connect(lambda: self.edit_name_page.CreateWindow(self.name))  # Назначение действия при нажатии на кнопку редактирования имени
        self.edit_name_page.save_name_button.clicked.connect(lambda: self.UpdateName())  # Назначение действия при нажатии на кнопку сохранения имени                                                                             # (кнопка расположена на виджете изменения имени)

        self.UpdateData()  # Обновить данные окна
        self.window().show()  # Показать текущее окно

    def CloseWindow(self):  # Метод для сокрытия окна
        self.window().hide()  # Спрятать текущее окно

    def AddNote(self):  # Метод для создания новой 'пустой' заметки
        if len(self.notes) < 40:  # Если общее кол-во заметок < 40
            self.notes.append(Note('title', 'text', 'Job_in_progress', 0))  # К списку заметок добавить новую
            self.UpdateData()  # Обновить данные окна

    def CreateNote(self, number, note):  # Метод для отрисовки заметки; кнопок редактирования и удаления заметки и шкалы прогресса на фрейме с заметками
        self.layout.setRowMinimumHeight(len(self.notes) // 4, 450)  # Задаём минимальную высоту столбца на сетке
        self.layout.setRowStretch(len(self.notes) // 4, 1)  # Задаём возможность изменения размера столбца сетки
        frame = QLabel(self.notes_board)  # Создаём новый frame
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        frame.setMinimumSize(400, 450)  # Задаём минимальные размеры для frame
        self.layout.addWidget(frame, number // 4, number % 4)  # Добавляем frame в сетку

        label = QLabel(frame)  # Создаём новый label
        label.setGeometry(0, 0, 400, 450)  # Задаём его позицию и размеры
        if note.type == 'Job_is_done':                           # Создаём
            label.setPixmap(QPixmap('static/img/Job_is_done.png'))       # внешний вид
        if note.type == 'Job_in_progress':                       # заметки
            label.setPixmap(QPixmap('static/img/Job_in_progress.png'))   # в зависимости от
        if note.type == 'Job_is_cancelled':                      # её
            label.setPixmap(QPixmap('static/img/Job_is_cancelled.png'))  # типа

        title_label = QLabel(frame)  # Создаём полу для отображения оглавления заметки
        title_label.setGeometry(70, 60, 180, 40)  # Задаём его позицию и размеры
        title_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)  # Задаём привязку текста к левому краю по горизонтали и к верхнему - по горизонтали
        title_label.setWordWrap(True)  # Сделать перенос слов в поле с оглавлением
        title_label.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: #fbfd53;')  # Делаем прозрачный фон и жёлтый текст в поле с оглавлением
        title_label.setFont(QFont('Calibri', 20, QFont.Bold))  # Настраиваем шрифт в поле с оглавлением
        title_label.setText(note.title)  # Размещаем текст оглавления в поле для оглавления

        text_label = QLabel(frame)  # Создаём поля для отображения текста заметки
        text_label.setGeometry(70, 100, 180, 225)  # Задаём его позицию и размеры
        text_label.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)  # Задаём привязку текста к левому краю по горизонтали и к верхнему - по горизонтали
        text_label.setWordWrap(True)  # Сделать перенос слов в поле с текстом
        text_label.setStyleSheet('background-color: rgba(0, 0, 0, 0); color: #fbfd53;')  # Делаем прозрачный фон и жёлтый текст в поле с текстом
        text_label.setFont(QFont('Calibri', 14))  # Настраиваем шрифт в поле с текстом
        text_label.setText(note.text)  # Размещаем текст в поле с текстом заметки

        edit_note_button = QPushButton(frame)  # Создаём кнопку для редактирования заметки
        edit_note_button.setGeometry(315, 50, 70, 70)  # Задаём позицию и размеры кнопки
        edit_note_button.setStyleSheet('border: none;')  # Убираем поля кнопки
        edit_note_button.setIcon(QIcon('static/img/edit_button.png'))  # Заугржаем иконку кнопки
        edit_note_button.setIconSize(QSize(70, 70))  # Задаём размеры иконки кнопки
        edit_note_button.clicked.connect(lambda: self.EditNote(number, note))  # Назначаем действие при нажатии на кнопку редактирования заметки

        delete_note_button = QPushButton(frame)  # Создаём кнопку для удаления заметки
        delete_note_button.setGeometry(315, 110, 70, 70)  # Задаём позицию и размеры кнопки
        delete_note_button.setStyleSheet('border: none;')  # Убираем поля кнопки
        delete_note_button.setIcon(QIcon('static/img/delete_button.png'))  # Заугржаем иконку кнопки
        delete_note_button.setIconSize(QSize(70, 70))  # Задаём размеры иконки кнопки
        delete_note_button.clicked.connect(lambda: self.DeleteNote(number))  # Назначаем действие при нажатии на кнопку удаления заметки

        progress_bar_label = QLabel(frame)  # Создаём label для шкалы прогресса
        progress_bar_label.setGeometry(310, 180, 100, 250)  # Задаём позицию и размеры
        pixmap = self.GetProgressBarImage(note.type, note.progress)  # Получаем изображение шкалы прогресса в зависимости от типа и прогресса заметки
        progress_bar_label.setPixmap(pixmap)  # Устанавливаем нужное изображение шкалы прогресса

    def DeleteNote(self, n):  # Метод для удаления заметки из списка по индексу n
        self.notes.pop(n)  # Удаляем заметку из списка по индексу
        self.UpdateData()  # Обновить данные окна

    def UpdateData(self):  # Метод для обновления данных окна
        for widget in self.notes_board.findChildren(QWidget):  # Перебираем каждый виджет с главного фрейма
            widget.deleteLater()  # Удаляем виджет
        if self.notes is not None:  # Если список заметок != None
            self.notes_board.setGeometry(150, (self.notes_board.pos()).y(), 1620, (len(self.notes)+1) // 4 * 500 + 800)  # Переместить главный фрейм с заметками
        if self.edit_name_page.GetNewName() != '':  # Если имя, расположенное на EditNameWidget - не пустая строка
            self.name = self.edit_name_page.GetNewName()  # Имя пользователя = имя, расположенное на EditNameWidget
            self.SetTextName()  # Размещение имени на панели приветствия пользователя в правом верхнем углу экрана
        if self.notes is not None:  # Если список заметок != None
            for i in range(len(self.notes)):  # Перебираем каждую заметку
                self.CreateNote(i, self.notes[i])  # Вызываем метод отрисовки заметки
        self.edit_name_button.clicked.connect(lambda: self.edit_name_page.CreateWindow(self.name))  # Переназначаем функцию для открытия окна редактирования имени
                                                                                                    # при нажатии на кнопку (необходимо для актуализации имени пользователя)

    def GetProgressBarImage(self, type, progress):  # Метод для получения изображения шкалы прогресса в зависимости от типа и прогресса заметки
        progress_bar_pixmap = None
        if type == 'Job_is_done':
            progress_bar_pixmap = QPixmap('static/img/full_green.png')
        elif progress < 10:
            progress_bar_pixmap = QPixmap('static/img/empty.png')
        elif type == 'Job_in_progress':
            if 10 <= progress < 20:
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
        elif type == 'Job_is_cancelled':
            if 10 <= progress < 20:
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

    def SetTextName(self):  # Метод для размещения имени пользователя в правом верхнем углу экрана (размещение по 16 символов в строку)
        if len(self.name) < 16:
            self.name_label.setText(f'Приветствуем,\n{self.name}!')
        elif 16 < len(self.name) < 32:
            self.name_label.setText(f'Приветствуем,\n{self.name[:16]}\n{self.name[16:32]}!')
        elif len(self.name) > 32:
            self.name_label.setText(f'Приветствуем,\n{self.name[:16]}\n{self.name[16:32]}\n'
                                    f'{self.user_data['name'][32:48]}!')

    def EditNote(self, number, note):  # Метод для открытия окна редактирования заметок
        edit_window = EditNoteWidget()  # Создание экземпляра класса окна редактирования заметок
        edit_window.CreateWindow(number, note)  # Открытие окна редактирования заметок
        edit_window.save_button.clicked.connect(lambda: self.UpdateNotes(edit_window))  # Назначение действий при нажатии на кнопку сохранения изменения заметки
                                                                                        # (кнопка расположена в окне редактирования заметок)

    def UpdateNotes(self, edit_window):  # Метод для сохранения изменений заметки
        self.notes[edit_window.number] = edit_window.GetUpdatedNote()  # заметка с указанным номером = заметка с окна редактирования заметки
        edit_window.CloseWindow()  # Скрыть окно редактирования заметки
        self.UpdateData()  # Обновить данные окна

    def UpdateName(self):  # Метод для обновления имени пользователя на главном окне
        self.name = self.edit_name_page.GetNewName()  # Получение переменной имени, находящейся в окне редактирования имени
        self.UpdateData()  # Обновить данные окна
        self.edit_name_page.CloseWindow()  # Закрыть окно редактирования имени

    def GetUserData(self):  # Метод для получения данных аккаунта с главного окна (используется другими классами)
        self.user_data['id'] = self.user_id   # Задать значение id аккаунта в данных аккаунта
        self.user_data['name'] = self.name    # Задать значение имени пользователя в данных аккаунта
        self.user_data['notes'] = self.notes  # Задать значение списка заметок в данных аккаунта
        return self.user_data  # Вернуть значение данных аккаунта

    def wheelEvent(self, event):  # Обработка события вращения колёсика мышки (при вращении колёсика мышки происходит croll фреёма с заметками)
        delta = event.angleDelta().y()  # Получить угол поворота колёсика мышки
        if (self.notes_board.pos()).y() + delta > 300:  # Проверка, можем ли мы переместить главный фрейм, чтобы он не вышел за нужные границы сверху
            self.notes_board.setGeometry(150, 300, 1620, (len(self.notes) // 4 + 1) * 450 + 500)  # Перемещаем главный фрейм с заметками к верхней границе
        elif (self.notes_board.pos()).y() + delta < -(len(self.notes) // 4 + 1) * 450 + 400:  # Проверка, можем ли мы переместить главный фрейм, чтобы он не вышел за нужные границы снизу
            self.notes_board.setGeometry(150, -(len(self.notes) // 4 + 1) * 450 + 400, 1620, (len(self.notes) // 4 + 1) * 450 + 500)  # Перемещаем главный фрейм с заметками к нижней границе
        else:
            self.notes_board.setGeometry(150, (self.notes_board.pos()).y() + delta, 1620, (len(self.notes) // 4 + 1) * 450 + 500)  # Перемещаем главный фрейм с заметками в новую позицию
