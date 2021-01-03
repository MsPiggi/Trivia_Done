import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, Pagination
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''

    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type, Authorization'
          )
        response.headers.add(
          'Access-Control-Allow-Methods',
          'GET, POST, PATCH, DELETE, OPTIONS'
          )
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories', methods=['GET'])
    def show_categories():
        categories = Category.query.all()
        formated_categories = {
          category.id: category.type for category in categories
          }

        return jsonify({
            'message': True,
            'categories': formated_categories,
            'currentCategory': None
            })

    '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and
    pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/questions', methods=['GET'])
    def show_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.all()
        formated_questions = [question.format() for question in questions]
        categories = Category.query.all()
        formated_categories = {
          category.id: category.type for category in categories
          }

        return jsonify({
          'message': True,
          'questions': formated_questions[start:end],
          'totalQuestions': len(formated_questions),
          'categories': formated_categories
          })

    '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            Question.query.filter_by(id=question_id).delete()
            db.session.commit()
        except expression:
            db.session.rollback()
        finally:
            db.session.close()
            return jsonify({
                'success': True
              })

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear
    at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        error = False
        new_question = request.json.get('question')
        new_answer = request.json.get('answer')
        new_difficulty = request.json.get('difficulty')
        new_category = request.json.get('category')

        try:
            db.session.add(Question(
              question=new_question,
              answer=new_answer,
              category=new_category,
              difficulty=new_difficulty
              ))

        except expression:
            abort(422)
            error = True

        finally:
            if not error:
                db.session.commit()
                return jsonify({
                  'success': True,
                  'message': "Sucessfully created"
                  })
            else:
                db.session.rollback()
                return jsonify({
                  'success': False,
                  })

    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        if not request.method == "POST":
            abord(405)

        data = request.get_json()
        search_term = data.get('searchTerm')

        if not search_term:
            abort(422)

        questions = Question.query.filter(
          Question.question.ilike('%{}%'.format(search_term))).all()

        formated_questions = [question.format() for question in questions]
        print(questions)

        if not questions:
            abort(422)

        return jsonify({
              'message': True,
              'questions': formated_questions,
              'totalQuestions': len(formated_questions),
          })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<category_id>/questions', methods=['GET'])
    def show_questions_by_category(category_id):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        questions = Question.query.filter_by(category=category_id).all()
        formated_questions = [question.format() for question in questions]
        categories = Category.query.all()
        formated_categories = {
          category.id: category.type for category in categories}

        return jsonify({
          'message': True,
          'questions': formated_questions[start:end],
          'totalQuestions': len(formated_questions),
          'categories': formated_categories,
          'currentCategory': category_id
          })

    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_quiz_questions():

        body = request.get_json()
        prev_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)
        try:
            if quiz_category['id'] == 0:
                quiz = Question.query.all()
            else:
                quiz = Question.query.filter_by(
                    category=quiz_category['id']).filter(
                    Question.id.notin_((prev_questions))).all()

            if not quiz:
                abort(422)

            selected = []

            for question in quiz:
                if question.id not in prev_questions:
                    selected.append(question.format())

            if len(selected) != 0:
                result = random.choice(selected)
                return jsonify({
                  'success': True,
                  'question': result,
                })
            else:
                return jsonify({
                  'success': False,
                  'question': result
                })

        except expression:
            abort(422)

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(404)
    def bad_request(error):
        return jsonify({
          "success": False,
          "error": 404,
          "message": "File Not Found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable Entity"
        }), 422

    return app

    if __name__ == '__main__':
        app.run()
