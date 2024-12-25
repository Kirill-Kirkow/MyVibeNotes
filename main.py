from PyQt5 import QtWidgets
from RegisterWidget import RegisterWidget
import sys

# Вся программа запускается через файл main.py

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Создание программы
    window = RegisterWidget()  # Создание экземпляра класса окна регистрации (через это окно будут создаваться другие окна приложения)
    window.CreateWindow()  # Метод класса "Register widget", который отображает окно регистрации
    sys.exit(app.exec_())  # Запуск основного цикла приложения
