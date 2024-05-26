import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_hello_world(client):
    """Тест для маршрута по умолчанию."""
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == 'Hello World!'


def test_create_task(client):
    """Тест для создания новой задачи."""
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'Test Description'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['title'] == 'Test Task'
    assert data['description'] == 'Test Description'


def test_create_task_without_description(client):
    """Тест для создания новой задачи без описания."""
    response = client.post('/tasks', json={
        'title': 'Task Without Description'
    })
    data = response.get_json()

    assert response.status_code == 201
    assert data['title'] == 'Task Without Description'
    assert data['description'] is None


def test_create_task_without_title(client):
    """Тест для попытки создания задачи без названия."""
    response = client.post('/tasks', json={
        'description': 'Description Without Title'
    })
    assert response.status_code == 400
    assert 'title' in response.get_json()


def test_get_tasks(client):
    """Тест для получения списка задач."""
    client.post('/tasks', json={'title': 'Task 1'})
    client.post('/tasks', json={'title': 'Task 2'})

    response = client.get('/tasks')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2


def test_get_task(client):
    """Тест для получения задачи."""
    response = client.post('/tasks', json={'title': 'Task 1'})
    task_id = response.get_json()['id']

    response = client.get(f'/tasks/{task_id}')
    data = response.get_json()
    assert data['title'] == 'Task 1'
    assert response.status_code == 200


def test_update_task(client):
    """Тест для обновления задачи."""
    response = client.post('/tasks', json={'title': 'Original Title'})
    task_id = response.get_json()['id']

    response = client.put(f'/tasks/{task_id}', json={
        'title': 'Updated Title',
        'description': 'Updated Description'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['title'] == 'Updated Title'
    assert data['description'] == 'Updated Description'


def test_delete_task(client):
    """Тест для удаления задачи."""
    response = client.post('/tasks', json={'title': 'Task to be deleted'})
    task_id = response.get_json()['id']

    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Task deleted successfully'

    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 404
