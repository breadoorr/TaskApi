from app import create_app, db

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()  # Создание всех таблиц в базе данных (если не существуют)

    app.run(debug=True)  # Запуск Flask-приложения в режиме отладки