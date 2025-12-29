# ToDo-Django(Django + Rest APi's + Templates)

->  This project is a Todo List web application built using Django and Django REST Framework,
    following RESTful principles.
->  It provides CRUD APIs for task management and uses Django templates integrated with APIs
    for the user interface.

# Important Things as per requirements
    Django ORM NOT used
    Generic ViewSets NOT used
    All database operations are performed using raw SQL

# Features
->  Create, read, update, and delete tasks (CRUD)
->  REST APIs using Django REST Framework (APIView)
->  Written test cases (APITestCase)
->  Django templates for UI
->  Templates interact with APIs using JavaScript
->  Raw SQL for database operations
->  Timestamp handling for due dates
->  Clean UI with basic CSS
->  Error handling and logging

# Tech Stack
    Backend   : Python, Django, Django REST Framework
    Frontend  : HTML, CSS, JavaScript
    Database  : SQLite
    API Style : REST
    No ORM / No Generic ViewSets

# File Tree
to_do_list
 ┣ to_do_list
 ┃ ┣ asgi.py
 ┃ ┣ settings.py
 ┃ ┣ urls.py
 ┃ ┗ wsgi.py
 ┣ todo
 ┃ ┣ templates
 ┃ ┃ ┗ todo
 ┃ ┃ ┃ ┣ add_task.html
 ┃ ┃ ┃ ┗ list_task.html
 ┃ ┣ admin.py
 ┃ ┣ apps.py
 ┃ ┣ models.py
 ┃ ┣ serializers.py
 ┃ ┣ tests.py
 ┃ ┣ urls.py
 ┃ ┗ views.py
 ┣ db.sqlite3
 ┣ django.log
 ┗ manage.py

# Setup and Instructions

#   Clone the repo
        git clone <My Repo>
        cd TODO-DJANGO
#   Create and activate virtual environment
        python3 -m venv venv
        source venv/bin/activate   <!--In case of linux/macos -->
#   Install Dependencies
        pip install django djangorestframework
#   DataBase Setup(Since Django ORM is not used in this project, the database table must be created manually using the Django Python shell.)
        cd to_do_list
        python3 manage.py shell
        <!-- Inside Shell -->
       >from django.db import connection

       >with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS task (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date INTEGER,
                    status TEXT
                );
            """)
       >exit()
#   Run the Server
        python3 manage.py runserver
#   Open the Browser
        http://127.0.0.1:8000/

# Run Test case
    python3 manage.py test todo

# API End Points
#   Get all task
        EndPoint GET: /api/tasks
        Sample Response(JSON):
            [
                {
                    "id": 7,
                    "title": "abcdefg",
                    "description": "hello",
                    "due_date": 1728000000,
                    "status": "pending"
                },
                {
                    "id": 6,
                    "title": "abcd",
                    "description": "hello",
                    "due_date": 1767100168,
                    "status": "pending"
                }
            ]
#   Create a Task
        Endpoint POST: /api/tasks/
        Payload(JSON):
            {
                "title": "abcd",
                "description": "hello",
                "due_date": 1767100168,
                "status": "pending"
            }
        Response:
            {
                "message": "Task created successfully",
                "id": 7
            }
#   Update a task
        EndPoint PUT: /api/tasks/{id}/
        Payload(JSON):
            {
                "title": "abcd",
                "description": "hello",
                "due_date": 1767100168,
                "status": "pending"
            }
        Response:
            {
                "messgae": "Task updated Successfully"
            }
#   Delete a task
        EndPoint DELETE": /api/tasks/{id}/
        Response{JSON}:
            {
                "message": "Task deleted successfully"
            }

# Author
# Nishant Sharma(Python/Software Developer)
