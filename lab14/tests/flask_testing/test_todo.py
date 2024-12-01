from flask import url_for
from .base_test import BaseTest
from app.todo.models import Todo
from app import db
from datetime import date

class TodoTest(BaseTest):

    def setUp(self):
        super().setUp()
        db.session.add(Todo(title="TODO tests", due_date=date(2023, 12, 14), complete=False))
        db.session.commit()

    def test_view_todo_page(self):
        '''Ensures all todos were displayed on the page'''

        todo_1 = Todo(title="Test todo 1", due_date=date(2023, 12, 14), complete=False)
        todo_2 = Todo(title="Test todo 2", due_date=date(2023, 12, 13), complete=False)
        db.session.add_all([todo_1, todo_2])

        response = self.client.get(url_for('todo.todo_page'))

        self.assertIn(f"{todo_1.title}".encode(), response.data)
        self.assertIn(f"{todo_2.title}".encode(), response.data)
        self.assertIn(b"Things I must To Do", response.data)
        self.assertIn(b"TODO tests", response.data)
        self.assertEqual(Todo.query.count(), 3)

    def test_create(self):
        '''Ensures a new todo is created successfully'''

        with self.client:
            response = self.client.post(
                url_for('todo.add'),
                data=dict(title='Test task', due_date='2023-12-13'),
                follow_redirects=True
            )
            self.assert200(response)
            self.assertMessageFlashed("Todo added!", 'success')

            todo = Todo.query.filter_by(title='Test task').first()

            self.assertEqual(todo.due_date, date(2023, 12, 13))
            self.assertFalse(todo.complete)

    def test_update_complete(self):
        '''Ensures a todo is marked as complete successfully'''

        todo = Todo.query.filter_by(title="TODO tests").first()

        with self.client:
            response = self.client.get(
                url_for('todo.update', id=todo.id),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertMessageFlashed(f'Todo({todo.id}) updated!', 'success')
            self.assertTrue(todo.complete)

    def test_update_incomplete(self):
        '''Ensures a todo is marked as incomplete successfully'''

        todo = Todo.query.filter_by(title="TODO tests").first()
        todo.complete = True
        db.session.commit()

        with self.client:
            response = self.client.get(
                url_for('todo.update', id=todo.id),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertMessageFlashed(f'Todo({todo.id}) updated!', 'success')
            self.assertFalse(todo.complete)

    def test_delete(self):
        '''Ensures a todo is deleted successfully'''

        todo = Todo.query.filter_by(title="TODO tests").first()

        with self.client:
            response = self.client.get(
                url_for('todo.delete', id=todo.id),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertMessageFlashed(f'Todo({todo.id}) deleted!', 'success')
            self.assertIsNone(Todo.query.filter_by(title="TODO tests").first())

    def test_delete_fail(self):
        '''Ensures a 404 error is generated when deleting a non-existent todo'''
        with self.client:
            response = self.client.get(
                url_for('todo.delete', id=5),
                follow_redirects=True
            )
            self.assert404(response)