from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from DataBase import DbActions
from MainWindow import MainWindow

# В данном файле прописан класс работы окна регистрации

class RegisterWidget(QWidget):  # Класс окна регистрации
    def __init__(self):
        super(RegisterWidget, self).__init__()
        uic.loadUi('static/ui/RegisterWidget.ui', self)  # Импорт ui файла
        self.data_base = DbActions()  # Создание экземпляра класса DbActions для взаимодействий с БД
        self.register_button.clicked.connect(lambda: self.OnRegisterButtonClick())  # Назначение действий при нажатии на кнопку регистрации
        self.login_button.clicked.connect(lambda: self.OnLoginButtonClick())  # Назначение действий при нажатии на кнопку входа в аккаунт
        self.main_window = MainWindow()  # Создание экземпляра главного окна программы
        self.main_window.exit_button.clicked.connect(lambda: self.ExitMainWindow())  # Назначение действий при нажатии на кнопку выхода из аккаунта (находится на главном окне программы)

    def OnRegisterButtonClick(self):  # Действия при нажатии на кнопку регистрации
        data = self.data_base.Register(self.login_input_field.text(), self.password_input_field.text())  # Получение 'Отклика' от функции регистрации в классе DbActions
        if data == 'Данный логин уже существует' or data == 'Логин должен содержать минимум 3 символа':  # Обработка неверно введённого логина
            self.login_input_field.setStyleSheet('border: 1px solid #ff0000; '
                                                 'background-color: rgba(250, 250, 250, 255); '
                                                 'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода логина красным цветом
            self.login_error_text.setText(data)  # Выведение текста ошибки на панели ошибок ввода логина

            self.password_input_field.setStyleSheet('border: 1px solid #404040;'
                                                    'background-color: rgba(250, 250, 250, 255);'
                                                    'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода пароля обычным цветом
            self.password_error_text.setText('')  # Очищение текста с панели ошибок ввода пароля
        elif data == 'Пароль должен содержать минимум 8 символов':  # Обработка неверно введённого пароля
            self.login_input_field.setStyleSheet('border: 1px solid #404040;'
                                                 'background-color: rgba(250, 250, 250, 255);'
                                                 'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода логина обычным цветом
            self.login_error_text.setText('')  # Очищение текста с панели ошибок ввода логина

            self.password_input_field.setStyleSheet('border: 1px solid #ff0000;'
                                                    'background-color: rgba(250, 250, 250, 255);'
                                                    'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода пароля красным цветом
            self.password_error_text.setText(data)  # Выведение текста ошибки на панели ошибок ввода пароля
        else:  # Действия в случае правильной регистрации пользователя
            self.login_input_field.setStyleSheet('border: 1px solid #00ff00;'
                                                 'background-color: rgba(250, 250, 250, 255);'
                                                 'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода логина обычным цветом
            self.login_error_text.setText('')  # Очищение текста с панели ошибок ввода логина

            self.password_input_field.setStyleSheet('border: 1px solid #00ff00;'
                                                    'background-color: rgba(250, 250, 250, 255);'
                                                    'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода пароля обычным цветом
            self.password_error_text.setText('')  # Очищение текста с панели ошибок ввода пароля

            self.main_window.CreateWindow(data)  # Показать главное окно программы и передать в него данные об аккаунте
            self.CloseWindow()  # Спрятать текущее окно

    def OnLoginButtonClick(self):  # Действия при нажатии на кнопку авторизации
        data = self.data_base.Login(self.login_input_field.text(), self.password_input_field.text())  # Получение 'Отклика' от функции авторизации в классе DbActions
        if data == 'Неверный логин':  # Действия при неправильно введённом логине
            self.login_input_field.setStyleSheet('border: 1px solid #ff0000; '
                                                 'background-color: rgba(250, 250, 250, 255); '
                                                 'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода логина красным цветом
            self.login_error_text.setText(data)  # Выведение текста ошибки на панели ошибок ввода логина

            self.password_input_field.setStyleSheet('border: 1px solid #404040;'
                                                    'background-color: rgba(250, 250, 250, 255);'
                                                    'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода пароля обычным цветом
            self.password_error_text.setText('')  # Очищение текста с панели ошибок ввода пароля
        elif data == 'Неверный пароль':  # Действия при неправильно введённом пароле
            self.login_input_field.setStyleSheet('border: 1px solid #404040;'
                                                 'background-color: rgba(250, 250, 250, 255);'
                                                 'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода логина обычным цветом
            self.login_error_text.setText('')  # Очищение текста с панели ошибок ввода логина

            self.password_input_field.setStyleSheet('border: 1px solid #ff0000;'
                                                    'background-color: rgba(250, 250, 250, 255);'
                                                    'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода пароля красным цветом
            self.password_error_text.setText(data)  # Выведение текста ошибки на панели ошибок ввода пароля
        else:  # Действия при успешной авторизации
            self.login_input_field.setStyleSheet('border: 1px solid #00ff00;'
                                                 'background-color: rgba(250, 250, 250, 255);'
                                                 'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода логина обычным цветом
            self.login_error_text.setText('')  # Очищение текста с панели ошибок ввода логина

            self.password_input_field.setStyleSheet('border: 1px solid #00ff00;'
                                                    'background-color: rgba(250, 250, 250, 255);'
                                                    'color: rgba(5, 5, 5, 255);')  # Обводка поля ввода пароля обычным цветом
            self.password_error_text.setText('')  # Очищение текста с панели ошибок ввода пароля
            self.main_window.CreateWindow(data)  # Показать главное окно программы и передать в него данные об аккаунте
            self.CloseWindow()  # Спрятать текущее окно

    def CreateWindow(self):  # Метод для отображения окна
        self.window().show()  # Показать текущее окно
        self.data_base.ConnectDb()  # Подключиться к БД

    def CloseWindow(self):  # Метод для сокрытия окна
        self.data_base.CloseDb()  # Закрыть подключение с БД
        self.window().hide()  # Спрятать окно

    def ExitMainWindow(self):  # Метод для вызова при нажатии пользователем на кнопку выхода из аккаунта (находится на главном окне)
        data = self.main_window.GetUserData()  # получение обновлённых данных аккаунта из главного окна
        self.main_window.CloseWindow()  # спрятать главное окно
        self.data_base.ConnectDb()  # подключиться к БД
        self.data_base.UpdateData(data)  # внести изменения в БД
        self.data_base.CloseDb()  # закрыть подключение с БД
        self.CreateWindow()  # показать окно регистрации
