import sqlite3
from Note import Note

# Класс DbActions содержит методы для взаимодействия с базой данных (далее БД)

class DbActions:
    def __init__(self):
        self.data_base = None  # Файл БД
        self.cursor = None     # Курсор БД. Нужен для отправки SQL запросов в БД

    def ConnectDb(self):  # Метод для подключения к БД
        self.data_base = sqlite3.connect('db/database.db')  # Подключение к БД, если она существует и её создание, если не существует
        self.cursor = self.data_base.cursor()  # Назначаем курсор БД

        self.data_base.execute("PRAGMA foreign_keys = ON;")  # Включить использование внешних ключей в БД

        query_create_table_account = """CREATE TABLE IF NOT EXISTS accounts(
                                            id INTEGER PRIMARY KEY,
                                            login TEXT UNIQUE NOT NULL, 
                                            password TEXT NOT NULL)"""  # Запрос на создание таблицы 'accounts' с аккаунтами пользователей, если такой таблицы ещё нет в БД
        query_create_table_user = """CREATE TABLE IF NOT EXISTS users(
                                            id INTEGER PRIMARY KEY,
                                            name TEXT,
                                            notes_count INTEGER,
                                            FOREIGN KEY (id) REFERENCES accounts (id) ON DELETE CASCADE)""" # Запрос на создание таблицы 'users' с настройками аккаунтов пользователей, если такой таблицы ещё нет в БД
        query_create_table_notes = """CREATE TABLE IF NOT EXISTS notes(
                                            id INTEGER PRIMARY KEY, 
                                            user_id INTEGER, 
                                            title TEXT, 
                                            text TEXT, 
                                            type TEXT, 
                                            progress INTEGER,
                                            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE)""" # Запрос на создание таблицы 'notes', которая хранит в себе данные о всех заметках, если такой таблицы ещё нет в БД

        self.cursor.execute(query_create_table_account)  # Выполнение запросов на создание таблиц 'accouns', 'users' и 'notes' в БД
        self.cursor.execute(query_create_table_user)
        self.cursor.execute(query_create_table_notes)

        self.data_base.commit()  # Сохранить изменения в БД

    def Register(self, login, password):  # Функция, обрабатывающая регистрацию пользователя
        self.cursor.execute("""SELECT login FROM accounts WHERE login=(?)""",
                            (login,))  # Поиск логина в БД
        if self.cursor.fetchone() is None and len(password) >= 8 and len(login) >= 3:  # Действия, когда пользователь удачно регистрируется
                                                                                       # (в БД нет введённого логина, а пароль и логин имеют необходимую длинну)
            self.cursor.execute("""INSERT INTO accounts (login, password) VALUES (?, ?)""",
                                (login, password,))  # Запрос на создание нового аккаунта в БД
            self.data_base.commit()  # Сохранить изменения в БД

            self.cursor.execute("""SELECT id FROM accounts WHERE login=(?)""",
                                (login,))  # Запрос на получение id аккаунта пользователя
            new_account_id = self.cursor.fetchone()[0]  # 'Вычленяем' id аккаунта из полученного списка
            self.cursor.execute("""INSERT INTO users (id, name, notes_count) VALUES (?, ?, 1)""",
                                (new_account_id, login,))  # Создаём новую запись в таблице users под нового пользователя
            self.data_base.commit()  # Сохранить изменения в БД

            self.cursor.execute(
                """INSERT INTO notes (user_id, title, text, type, progress) VALUES 
                (?, 
                'Приветствуем!', 
                'В данной системе вы можете создавать заметки (кнопка внизу), редактировать их и удалять (кнопки справа от заметки), а также задавать тип и прогресс заметки (в меню редактирования\nХорошего дня!)', 
                'Job_is_done', 
                100)""",
                (new_account_id,))  # Создание приветственной заметки в БД
            self.data_base.commit()  # Сохранить изменения в БД

            return self.GetUserData(login)  # Передать данные пользователя

        elif len(password) < 8:  # Действия, если пароль пользователя слишком короткий
            return 'Пароль должен содержать минимум 8 символов'  # Возвращаем текст ошибки
        elif len(login) < 3:  # Действия, если логин пользователя слишком короткий
            return 'Логин должен содержать минимум 3 символа'  # Возвращаем текст ошибки
        else:  # Действия, когда логин в системе уже существует
            return 'Данный логин уже существует'  # Возвращаем текст ошибки

    def Login(self, login, password):  # Функция, обрабатывающая авторизацию пользователя
        self.cursor.execute("""SELECT password FROM accounts WHERE login=(?)""",
                            (login,))  # Поиск пароля по логину в БД
        check_password = self.cursor.fetchone()  # Найденный пароль
        if check_password is None:  # Если пароль не был найден, переменная check_password будет = None
            return 'Неверный логин'  # Возвращаем текст ошибки
        elif check_password[0] == password:  # Если пароль соответствует введённому
            return self.GetUserData(login)  # Передать данные пользователя
        else:
            return 'Неверный пароль'  # Возвращаем текст ошибки

    def GetUserData(self, login):  # Метод для получения данных пользователя по логину
        self.cursor.execute(
            """SELECT accounts.id, users.name FROM accounts LEFT JOIN users ON accounts.id=users.id 
            WHERE accounts.login=(?)""",
            (login,))  # Запрос в БД на получение id аккаунта и имени пользователя
        user_data = {}  # Создаём словарь с данными пользователя
        user_typle = self.cursor.fetchone()  # Переменная user_typle получает id аккаунта и имя пользователя в виде списка
        user_id, user_name = user_typle[0], user_typle[1]  # Назначение переменных
        user_data['id'] = user_id  # Внесение id аккаунта в словарь с данными пользователя
        user_data['name'] = user_name  # Внесение имени пользователя в словарь с данными пользователя

        self.cursor.execute("""SELECT title, text, type, progress FROM notes WHERE user_id=(?)""",
                            (user_id,))  # Запрос в БД на получение данных о заметках пользователя
        notes_data = self.cursor.fetchall()  # Получение всех записей
        notes = []  # Создаём список заметок
        for note in notes_data:
            notes.append(Note(note[0], note[1], note[2], note[3]))  # Заполнение списка заметок данными, полученными из БД
        user_data['notes'] = notes  # Внесение списка заметок в словарь с данными пользователя

        return user_data  # Возврат из функции данных пользователя в виде словаря

    def UpdateData(self, user_data):  # Метод для обновления данных в БД (вызывается при выходе пользователя из аккаунта)
        user_id = user_data['id']  # Получение нового id аккаунта
        name = user_data['name']  # Получение нового имени пользователя
        notes = user_data['notes']  # Получение обновлённого списка заметок пользователя
        self.cursor.execute("""DELETE FROM users WHERE id=(?)""",
                            (user_id,))  # Удаление пользователя из БД
        self.data_base.commit()  # Сохранить изменения в БД
        self.cursor.execute("""INSERT INTO users (id, name, notes_count) VALUES (?, ?, ?)""",
                            (user_id, name, len(notes)))  # Внесение данных о пользователе в БД
        for note in notes:
            self.cursor.execute("""INSERT INTO notes (user_id, title, text, type, progress) VALUES (?, ?, ?, ?, ?)""",
                                (user_id, note.title, note.text, note.type, note.progress))  # Внесение нового списка заметок в БД
        self.data_base.commit()  # Сохранить изменения в БД

    def CloseDb(self):  # Метод для закрытия соединения с БД
        self.data_base.close()
