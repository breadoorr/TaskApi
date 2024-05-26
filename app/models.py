from . import db
from datetime import datetime


class Task(db.Model):
    """Модель Task, представляющая таблицу задач в базе данных."""
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор задачи
    title = db.Column(db.String(80), nullable=False)  # Название задачи, обязательное поле
    description = db.Column(db.String(200), nullable=True)  # Описание задачи, необязательное поле
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата и время создания задачи
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)  # Дата и время последнего обновления задачи

    def __init__(self, title, description=None):
        """Инициализация экземпляра задачи."""
        self.title = title  # Присваивание названия задачи
        self.description = description  # Присваивание описания задачи (если есть)
