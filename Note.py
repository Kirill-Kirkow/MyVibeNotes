
# В данном файле расположен класс Note, который содержит в себе данные заметки

class Note:
    def __init__(self, note_title, note_text, note_type, progress):
        self.title = note_title   # Заголовок заметки
        self.text = note_text     # Текст заметки
        self.type = note_type     # Тип заметки
        self.progress = progress  # Прогресс заметки
