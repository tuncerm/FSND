# Full Stack Trivia API Documentation

## Purpose
To demonstrate we can build an api.


## API
It is a RESTFull api, built to serve. Accepts and responds in json format.

Base URL =  ```/```

### Endpoints

```
GET     '/categories'
        Gets all available categories.
        response format:
        {
            "success": True,
            "categories": {
                'id' : 'type',
                'id2': 'type2',
                '1'  : 'Science',
                '2'  : 'Art',
                '3'  : 'Geography',
                '4'  : 'History',
                '5'  : 'Entertainment',
                '6'  : 'Sports'
            }
        }


GET     '/questions'
        Gets questions. Ten (10) questions per page.
        Accepts 'page' as query parameter. 
        If not supplied defaults to 1.
        response format:
        {
            "success": True,
            "questions": [
                {
                    id = 1
                    question = "Some question?"
                    answer = "Good Answer!"
                    category = 5
                    difficulty = 2
                }
            ],
            "total_questions": 183,
            "categories": {
                'id' : 'type',
                'id2': 'type2'
            },
            "current_category": 4
        }
POST    '/questions'
        Creates a question.
        Accepts json body.
        Example:
        {
            question = "Some question?"
            answer = "Good Answer!"
            category = 5
            difficulty = 2
        }
        Response Format:
        {
            "success": True,
            "message": "Success",
            "question": {
                id = 1
                question = "Some question?"
                answer = "Good Answer!"
                category = 5
                difficulty = 2
            }
        }

DELETE  '/questions/:question_id'
        Deletes the question associated with the provided question_id.
        Response Format:
        {
            "success": True,
            "message": "Deleted!",
            "id": question_id
        }

POST    '/questions/search'
        Accepts a searchTerm in json body. Returns the questions that contains provided string.
        Example Request:
        {'searchTerm':'Some'}

        Response Format:
        {
            "success": True,
            "questions": [
                {
                    id = 1
                    question = "Some question?"
                    answer = "Good Answer!"
                    category = 5
                    difficulty = 2
                }
            ],
            "total_questions": 1,
            "current_category": 0
        }

GET     '/categories/:category_id/questions'
        Retrieves all the questions associated with the provided category_id.
        Response Format:
        {
            "success": True,
            "questions": [
                {
                    id = 1
                    question = "Some question?"
                    answer = "Good Answer!"
                    category = category_id
                    difficulty = 2
                }
            ],
            "total_questions": 1,
            "current_category": category_id
        }


POST    '/quizzes'
        Streams questions one at a time.
        Requires a quiz_category that has an 'id' property.
        Requires an array of question id's.
        Retrieves a question at a time.
        It is users responsibility to provide id's of previous questions.
        Sample request body:
        {'quiz_category': {'id': 0, 'type': 'click'}, 'previous_questions': []}
        Response Format:
        {
            "success": True,
            "question": {
                id = 1
                question = "Some question?"
                answer = "Good Answer!"
                category = 5
                difficulty = 2
            }
        }
```
### Errors
All 4XX and 5XX errors have the same format. 
A success value of false, a generic error code and a generic message.

```
    Sample 4XX:
    {
        "success": False,
        "error": 4XX,
        "message": "Sample message"
    }
    Sample 5XX:
    {
        "success": False,
        "error": 5XX,
        "message": "Sample message"
    }
```
