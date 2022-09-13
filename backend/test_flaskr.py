import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import db_name_test, db_user, db_password


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = db_name_test
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(db_user, db_password, 'localhost:5432', self.database_name)
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
    def test_get_questions_success(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])

    def test_get_questions_404(self):
        res = self.client().get('/questions?page=100', json={'questions':'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)

    def test_get_categories_success(self):
        res= self.client().get('/categories')
        data = json.loads(res.data)
        print(res, "test")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)  
     

    def test_get_categories_404(self):
        res= self.client().get('/categories/300')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'],False)

    def test_delete_question_404(self):
        res= self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    def test_delete_questions_success(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)

    def test_add_questions_success(self):
        res= self.client().post('/questions', json={'new_question': 'test'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_add_questions_422(self):
        res= self.client().post('/questions', json={'new_question': ''})
        data = json.loads(res.data)

        pass

    def test_search_questions_404(self):
        res = self.client().post('/questions/search', json = {'searchTerm': '0000'})
        data= json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)

    def test_search_question_sucess(self):
        res = self.client().post('/questions/search', json = {'searchTerm': 'movie'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_questions_by_categories_success(self):
        res = self.client().get('/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)

    def test_questions_by_categories_404(self):
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)         

    def test_play_the_quiz_success(self):
        quiz={
            "previous_questions":[90],
            "quiz_category":{
                "type": 'Science',
                'id':'1'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_play_quiz_422(self):
        quiz={
            "previous_questions":[18],
            "quiz_category":{
                "type": 'testest',
                'id':'544'
            }
        }
        res = self.client().post('/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()