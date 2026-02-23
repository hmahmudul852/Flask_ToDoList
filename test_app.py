import unittest
from app import app, db, Todo

class TodoTestCase(unittest.TestCase):
    def setUp(self):
        # Set up a test client and test database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_task(self):
        # Test adding a task
        response = self.app.post('/', data={'content': 'Test Task'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            task = Todo.query.filter_by(content='Test Task').first()
            self.assertIsNotNone(task)

    def test_add_empty_task(self):
        # Test adding an empty task
        response = self.app.post('/', data={'content': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    def test_delete_task(self):
        # Test deleting a task
        with app.app_context():
            task = Todo(content='Delete Me')
            db.session.add(task)
            db.session.commit()
            task_id = task.id
        response = self.app.get(f'/delete/{task_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            task = Todo.query.get(task_id)
            self.assertIsNone(task)

    def test_update_task(self):
        # Test updating a task
        with app.app_context():
            task = Todo(content='Old Content')
            db.session.add(task)
            db.session.commit()
            task_id = task.id
        response = self.app.post(f'/update/{task_id}', data={'content': 'New Content'}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        with app.app_context():
            task = Todo.query.get(task_id)
            self.assertEqual(task.content, 'New Content')

    def test_update_empty_task(self):
        # Test updating a task with empty content
        with app.app_context():
            task = Todo(content='Old Content')
            db.session.add(task)
            db.session.commit()
            task_id = task.id
        response = self.app.post(f'/update/{task_id}', data={'content': ''}, follow_redirects=True)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
