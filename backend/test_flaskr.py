import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_type = 'postgres'
        self.database_code = 'Coding2!su'
        self.database_host = 'localhost:5432'
        self.database_path = "postgres://{}:{}@{}/{}".format(self.database_type, self.database_code , self.database_host , self.database_name)
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
    def test_db_exists(self):
        res = self.client().get('/')


    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], True)
        self.assertTrue(data['questions'])
        
    def test_show_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], True)
        self.assertTrue(data['categories'])

    def test_create_question(self):
                
        post_data = {
            'question': 'Who is the coolest Avatar?',
            'answer': 'Kora',
            'category': '5',
            'difficulty': 1
            }
        
        res = self.client().post('/questions', json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Sucessfully created")

    def test_delete_question(self):    
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
       
    def test_get_question_by_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['message'], True)
        self.assertEqual(data['currentCategory'], "1")

    def test_get_quiz_questions(self):
        post_data = {
            'quiz_category':
                {'id': "3",
                "type": "Geography",
                 }
            }

        res = self.client().post("/quizzes", json=post_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['question']) !=0)
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()