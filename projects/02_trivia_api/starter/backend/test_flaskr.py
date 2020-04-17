import unittest
import json

from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['categories'])

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), 10)

    def test_get_questions_invalid_page(self):
        res = self.client().get('/questions?page=100000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_create_question(self):
        new_question = {
            'question': 'Which?',
            'answer': 'One',
            'category': 6,
            'difficulty': 2
        }
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['question']['question'], new_question['question'])
        self.assertTrue(data['question']['id'])


    def test_delete_question(self):
        new_question = {
            'question': 'Which?',
            'answer': 'One',
            'category': 6,
            'difficulty': 2
        }
        res = self.client().post('/questions', json=new_question)
        id = json.loads(res.data)['question']['id']

        delete_res = self.client().delete(f'/questions/{id}')
        data = json.loads(delete_res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['id'], id)
        self.assertEqual(data['message'], 'Deleted!')

    def test_search(self):
        res = self.client().post('/questions/search', json={'searchTerm': ''})
        searchData = json.loads(res.data)

        res2 = self.client().get('/questions')
        questions_data = json.loads(res2.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(searchData['success'])
        self.assertTrue(questions_data['success'])
        self.assertEqual(searchData['total_questions'], questions_data['total_questions'])


    def test_quiz(self):
        json_data = {'quiz_category': {'id': 0, 'type': 'click'}, 'previous_questions': []}
        res = self.client().post('/quizzes', json=json_data)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
