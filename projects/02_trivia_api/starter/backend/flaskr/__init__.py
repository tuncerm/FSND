import random

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from models import setup_db, Category, Question

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after
    completing the TODOs
    '''
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    '''
    @DONE:
    Create an endpoint to handle GET requests for all available categories.
    '''

    @app.route('/categories')
    def get_categories():
        categories = {item['id']: item['type'] for item in
                      [category.format() for category in Category.query.all()]}

        return jsonify({
            "success": True,
            "categories": categories
        })

    '''
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three
    pages.
    Clicking on the page numbers should update the questions.
    '''

    def paginate_questions(page, selection):
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        current_category = request.args.get('category')
        questions = Question.query.order_by(Question.id).filter_by(
            category=current_category).all() if current_category is not None\
            else Question.query.order_by(Question.id).all()
        questions_in_page = paginate_questions(page, questions)
        categories = {item['id']: item['type'] for item in
                      [category.format() for category in Category.query.all()]}
        if len(questions_in_page) is 0:
            abort(404)

        return jsonify({
            "success": True,
            "questions": questions_in_page,
            "total_questions": len(questions),
            "categories": categories,
            "current_category": current_category
        })

    '''
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will
    be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if not question:
            abort(404)

        try:
            question.delete()
        except ex:
            abort(422)

        return jsonify({
            "success": True,
            "message": "Deleted!",
            "id": question_id
        })

    '''
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last
    page of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        if ('question' not in body) or ('answer' not in body) or \
           ('category' not in body) or ('difficulty' not in body):
            abort(400)
        new_question = Question(
            question=body['question'], answer=body['answer'],
            category=body['category'], difficulty=body['difficulty'])
        try:
            new_question.insert()
        except ex:
            abort(422)
        return jsonify({
            "success": True,
            "message": "Success",
            "question": new_question.format()
        })

    '''
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    @app.route('/questions/search', methods=['POST'])
    def question_search():
        search_term = request.get_json()['searchTerm']
        questions = Question.query.filter(
            Question.question.like(f"%{search_term}%")).all()
        return jsonify({
            "success": True,
            "questions": [item.format() for item in questions],
            "total_questions": len(questions),
            "current_category": None
        })

    '''
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_of_category(category_id):
        questions = Question.query.order_by(Question.id).filter_by(
            category=category_id).all()
        return jsonify({
            "success": True,
            "questions": [q.format() for q in questions],
            "total_questions": len(questions),
            "current_category": category_id
        })

    '''
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        body = request.get_json()
        quiz_category = body['quiz_category']['id']
        previous_questions = body['previous_questions']
        questions = Question.query.order_by(Question.id).filter_by(
            category=quiz_category).all() if quiz_category is not 0 else \
            Question.query.order_by(Question.id).all()

        qlist = []

        for q in questions:
            if q.id not in previous_questions:
                qlist.append(q.format())

        return jsonify({
            "success": True,
            "question": random.choice(qlist) if len(qlist) is not 0 else None
        })

    '''
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def not_my_fault(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request!"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found!"
        }), 404

    @app.errorhandler(405)
    def not_allowed_method(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed!"
        }), 405

    @app.errorhandler(422)
    def not_processable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable!"
        }), 422

    @app.errorhandler(500)
    def not_your_fault(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error!"
        }), 500

    return app
