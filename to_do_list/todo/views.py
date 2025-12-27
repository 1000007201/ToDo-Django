from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
# from datetime import datetime

class TaskView(APIView):

    # GET Request
    def get(self, request):
        '''
        GET Request for getting all records present in our table task
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT id, title, description, due_date, status
                    FROM task
                    ORDER BY id DESC
                    ''')
                data = cursor.fetchall()
            
            TaskDataDict = [
                {
                    'id'          : i[0],
                    'title'       : i[1],
                    'description' : i[2],
                    'due_date'    : i[3],
                    'status'      : i[4]
                }
                for i in data
            ]
            return Response(TaskDataDict, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Not able to get data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST Request
    def post(self, request):
        '''
        POST request for adding a record in our task table
        '''
        Serializer = TaskSerializer(data=request.data)
        if not Serializer.is_valid():
            return Response(
                {"error": Serializer.error_messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            print(Serializer.validated_data)
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    INSERT INTO task (title, description, due_date, status)
                    VALUES (%s, %s, %s, %s)
                    ''',
                    [
                        Serializer.validated_data.get("title"),
                        Serializer.validated_data.get("description"),
                        Serializer.validated_data.get("due_date"),
                        # if not present adding current timestamp in milliseconds   
                        Serializer.validated_data.get("status", "pending")
                    ])
                return Response(
                    {"message": "Task created successfully"},
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            print(e)
            return Response(
                {"error": "Something went wrong in creating task"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, id):
        '''
        PUT Request to update a specific record in our table task
        param id: Id of a record in our DB to be updated
        '''
        Serializer = TaskSerializer(data=request.data)
        if not Serializer.is_valid():
            return Response(Serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                UPDATE SET title = %s, description = %s, due_date = %s, status = %s
                WHERE id = %s
                '''
                [
                    Serializer.validated_data.get('title'),
                    Serializer.validated_data.get('description'),
                    Serializer.validated_data.get('due_date'),
                    Serializer.validated_data.get('status'),
                    id
                ]
            )
            if cursor.rowcount == 0:
                return Response({"error", "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"messgae": "Task updated Successfully"}, status=status.HTTP_200_OK)

class TestView(APIView):

    def get(self, request):
        return Response({"message": "get request"}, status=status.HTTP_200_OK)
    
class TaskCountView(APIView):
    
    # GET Request
    def get(self, request):
        '''
        Give the count of records present in our task table
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT COUNT(*) FROM task
                    ''')
                Count = cursor.fetchone()[0]
            return Response({"count": Count}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Not able to get count"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
