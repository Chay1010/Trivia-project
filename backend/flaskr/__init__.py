import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, ressources = {'/': {'origin': '*'}})
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        reqponse.headers.add("Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS")
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_all_categories():
        categories = Category.query.all()

        category = {category.id: category.type for category in categories}

        return jsonify({
            "success": True,
            'categories': category,
            'total_categories': len(categories)
            })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    def pagination(request, selection):
        page = request.args.get("page", 1, type=int)
        start = (page-1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/questions')
    def get_all_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = pagination(request, selection)

        if len(current_questions) == 0:
            abort(404)

        try:
            categories = Category.query.all()
            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(selection),
                'categories': {category.id: category.type for category in categories},
                'current category':None
            })
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        question = Question.query.get(question_id)
        try:
            question.delete()
            return jsonify({
                "success": True
                })
        except:
            abort(404)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods = ['POST'])
    def add_questions():
        body = request.get_json()
        nquestion = body.get('question')
        new_answer = body.get('answer')
        new_category = body.get('category')
        difficulty_score = body.get('difficulty')

        try:
            new_question = Question(question = nquestion, answer = new_answer, category = new_category, difficulty = difficulty_score)
            new_question.insert()
            return jsonify({
                "success":True
                })
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def seach_question():
        body = request.get_json()
        search_term = body.get('searchTerm')

        test = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        if len(test) == 0:
            abort(404)
        return jsonify({
            "success":True,
            "questions": [question.format() for question in test],
            "total_questions": len(test)
            })
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_categories(id):
        category = Category.query.get(id)

        if category : 
            questions = Question.query.filter(Question.category == str(id)).all()
            current_questions = pagination(request, questions)

        try:
            return jsonify({
                "success":True,
                "questions":current_questions,
                "total_questions": len(questions),
                "current category": category.type
                })
        except: 
            abort(404)
    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body.get('previous_questions')
        category = body.get('quiz_category')
        category_id = category['id']

        if category_id ==0:
            questions = Question.query.filter(Question.id.notin_(previous_questions)).all()

        else:
            questions = Question.query.filter(Question.category == category_id, Question.id.notin_(previous_questions)).all()

        if len(questions) == 0:
            abort(404)

        try:
            question = random.choice(questions)

            return jsonify({
                "success": True,
                "question": question.format()
                })
        except:
            abort(422)


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (jsonify({
            "success":False,
            "message": "ressource not found",
            "error": 404
            }),404)

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success":False,
            "error": 422,
            "message": "unprocessable"
            })

    return app

