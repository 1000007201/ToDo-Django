from rest_framework.test import APITestCase
from django.db import connection

class TaskAPITest(APITestCase):

    def setUp(self):
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                CREATE TABLE task (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date INTEGER,
                status TEXT
                );
                '''
            )
            cursor.execute(
                "INSERT INTO task (title, description, status) VALUES (%s, %s, %s)",
                ["Unit Test", "It is a test", "pending"]
            )
            self.TaskID = cursor.lastrowid

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute("DELETE from task")

    def test_get_tasks(self):
        Response = self.client.get("/api/tasks/")
        self.assertEqual(Response.status_code, 200)
        self.assertEqual(Response.data[0]["title"], "Unit Test")
    
    def test_post_tasks(self):
        Payload  = {"title": "Demo Todo", "status": "pending"}
        Response = self.client.post('/api/tasks/', Payload, format="json")
        self.assertEqual(Response.status_code, 201)

    def test_put_tasks(self):
        Payload  = {"title": "Demo Todo", "status": "completed"}
        Response = self.client.put(f'/api/tasks/{self.TaskID}', Payload, format="json")
        self.assertEqual(Response.status_code, 200)

    def test_delete_tasks(self):
        Response = self.client.delete(f'/api/tasks/{self.TaskID}')
        self.assertEqual(Response.status_code, 200)   
