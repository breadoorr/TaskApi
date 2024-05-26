from flask import request, jsonify
from .models import Task, db
from . import ma
from datetime import datetime
from marshmallow import ValidationError, validates, fields

class TaskSchema(ma.Schema):
    """Схема Marshmallow для сериализации и десериализации экземпляров Task."""
    class Meta:
        fields = ('id', 'title', 'description', 'created_at', 'updated_at')  # Определение полей для сериализации

    title = fields.String(required=True, validate=lambda s: len(s) > 0)  # Поле title, обязательное, с валидацией на непустое значение
    description = fields.String(required=False, allow_none=True)  # Поле description, необязательное, может быть None

    @validates('title')
    def validate_title(self, value):
        """Пользовательская валидация поля title, чтобы оно не было пустым."""
        if not value:
            raise ValidationError('Title is required and cannot be empty.')  # Ошибка валидации, если поле пустое


# Инициализация экземпляров схем
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


def init_routes(app):

    @app.route('/')
    def hello_world():
        """Маршрут по умолчанию для проверки работы API."""
        return jsonify('Hello World!'), 200

    @app.route('/tasks', methods=['POST'])
    def create_task():
        """Маршрут для создания новой задачи."""
        try:
            data = task_schema.load(request.json)  # Загрузка и валидация данных из запроса
        except ValidationError as err:
            return jsonify(err.messages), 400  # Возврат ошибок валидации, если данные неверные

        new_task = Task(**data)  # Создание новой задачи с валидированными данными
        db.session.add(new_task)  # Добавление новой задачи в сессию базы данных
        db.session.commit()  # Коммит изменений в базу данных

        return task_schema.jsonify(new_task), 201  # Возврат созданной задачи и статус кода 201

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        """Маршрут для получения всех задач."""
        tasks = Task.query.all()  # Получение всех задач из базы данных
        return tasks_schema.jsonify(tasks), 200  # Сериализация и возврат задач

    @app.route('/tasks/<int:id>', methods=['GET'])
    def get_task(id):
        """Маршрут для получения всех задач."""
        task = Task.query.get_or_404(id) # Получение всех задач из базы данных
        return task_schema.jsonify(task), 200  # Сериализация и возврат задач

    @app.route('/tasks/<int:id>', methods=['PUT'])
    def update_task(id):
        """Маршрут для обновления существующей задачи."""
        task = Task.query.get_or_404(id)  # Получение задачи по ID или возврат 404, если не найдено
        try:
            data = task_schema.load(request.json,
                                    partial=True)  # Загрузка и валидация данных из запроса (частичное обновление)
        except ValidationError as err:
            return jsonify(err.messages), 400  # Возврат ошибок валидации, если данные неверные

        for key, value in data.items():
            setattr(task, key, value)  # Обновление полей задачи новыми значениями
        task.updated_at = datetime.utcnow()  # Обновление времени последнего изменения задачи

        db.session.commit()  # Коммит изменений в базу данных
        return task_schema.jsonify(task), 200  # Сериализация и возврат обновленной задачи

    @app.route('/tasks/<int:id>', methods=['DELETE'])
    def delete_task(id):
        """Маршрут для удаления задачи."""
        task = Task.query.get_or_404(id)  # Получение задачи по ID или возврат 404, если не найдено
        db.session.delete(task)  # Удаление задачи из базы данных
        db.session.commit()  # Коммит изменений в базу данных
        return jsonify({'message': 'Task deleted successfully'}), 200  # Возврат сообщения об успешном удалении
