from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Инициализация расширений
db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    """Фабричная функция для создания и настройки Flask-приложения."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Настройка URI для подключения к базе данных
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключение отслеживания модификаций для повышения производительности

    db.init_app(app)  # Инициализация SQLAlchemy с приложением
    ma.init_app(app)  # Инициализация Marshmallow с приложением

    with app.app_context():
        db.create_all()  # Создание всех таблиц в базе данных (если не существуют)

    from .routes import init_routes
    init_routes(app)

    return app
