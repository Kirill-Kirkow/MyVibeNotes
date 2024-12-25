from PyQt5 import uic, QtCore, Qt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QDialog

# В данном файле прописан класс работы виджета для изменения имени пользователя

class EditNameWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('static/ui/EditNameWidget.ui', self)  # Импорт ui файла
        self.name = None  # Имя отображаемое на виджете
        self.delete_name_button.clicked.connect(lambda: self.DeleteName())  # Назначение действий при нажатии на кнопку удаления именим

    def CreateWindow(self, name):  # Метод для отображения окна
        self.name = name  # Задаём внутренней переменной имени пользователя в классе значение имени пользователя
        self.name_input_field.setText(self.name)  # Отображаем имя пользователя на панели ввода имени
        self.window().show()  # Показать текущее окно

    def DeleteName(self):  # Функция для стирания имени (при нажатии на кнопку)
        self.name = ''  # Внутренней переменной имени пользователя присваиваем пустую строку
        self.name_input_field.setText(self.name)  # Отображаем пустую строку на панели ввода имени

    def GetNewName(self):  # Метод для получения текущего имени пользователя из этого класса (используется другими классами)
        self.name = self.name_input_field.text()  # Внутренней переменной имени пользователя присваиваем значение с поля для ввода имени
        return self.name  # Возвращаем внутреннюю переменную имени пользователя

    def CloseWindow(self):  # Метод для сокрытия окна
        self.window().hide()  # Спрятать текущее окно
