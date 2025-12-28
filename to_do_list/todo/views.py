from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TaskSerializer
import logging

# For Templates
from django.shortcuts import render

# Getting logger for our todo app
logger = logging.getLogger("todo")

class TaskView(APIView):

    # GET Request
    def get(self, request, id=None):
        '''
        GET Request for getting all records present in our table task
        '''
        try:
            with connection.cursor() as cursor:
                if id is None:
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
                    logger.info(f"Fetched {len(TaskDataDict)} todos")
                    return Response(TaskDataDict, status=status.HTTP_200_OK)
                else:
                    cursor.execute(
                    '''
                    SELECT id, title, description, due_date, status
                    FROM task WHERE id = %s
                    ''',
                    [id]
                    )
                    data     = cursor.fetchone()
                    DataDict = [
                        {
                            'id'          : data[0],
                            'title'       : data[1],
                            'description' : data[2],
                            'due_date'    : data[3],
                            'status'      : data[4]
                        }
                    ]
                    logger.info(f"Fetched {len(DataDict)} todos")
                    return Response(DataDict, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Something went wrong while getting data Exception: {e}")
            return Response({"error": "Not able to get data"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # POST Request
    def post(self, request):
        '''
        POST request for adding a record in our task table
        '''
        Serializer = TaskSerializer(data=request.data)
        if not Serializer.is_valid():
            logger.info(f"Not able to add record in task reason {Serializer.error_messages}")
            return Response(
                {"error": Serializer.error_messages},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
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
                        Serializer.validated_data.get("status", "pending")
                    ])
                TaskID = cursor.lastrowid
                logger.info("Added Record to task table")
                return Response(
                    {"message": "Task created successfully", "id": TaskID},
                    status=status.HTTP_201_CREATED
                )

        except Exception as e:
            logger.error(f"Some exception occured while adding data Exception: {e}")
            return Response(
                {"error": "Something went wrong in creating task"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, id):
        '''
        PUT Request to update a specific record in our table task
        param id: Id of a record in our DB to be updated
        '''
        try:
            Serializer = TaskSerializer(data=request.data)
            if not Serializer.is_valid():
                logger.info(f"Not able to update record in task reason: {Serializer.error_messages}")
                return Response(Serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    UPDATE task SET title = %s, description = %s, due_date = %s, status = %s
                    WHERE id = %s
                    ''',
                    [
                        Serializer.validated_data.get('title'),
                        Serializer.validated_data.get('description'),
                        Serializer.validated_data.get('due_date'),
                        Serializer.validated_data.get('status'),
                        id
                    ]
                )
                if cursor.rowcount == 0:
                    logger.info("Task not found while updating")
                    return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
                logger.info("Updated record in task table")
                return Response({"messgae": "Task updated Successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Some exception occured while updating data Exception: {e}")
            return Response({"error": "Not able to update task"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE request 
    def delete(self, request, id):
        '''
        :param id: id of record want to delete from task table
        '''
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    DELETE FROM task WHERE id = %s
                    ''',
                    [
                        id
                    ]
                )
                if cursor.rowcount == 0:
                    logger.info("Task not found for Delete")
                    return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
            logger.info("Succesfully deleted task")
            return Response({"messgae": "Task deleted Successfully"}, status=status.HTTP_200_OK)
             
        except Exception as e:
            logger.error(f"Some exception occured while deleting data Exception: {e}")
            return Response({"error": "Not Able to delete Task"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
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
            logger.info("Successfully got total number of tasks")
            return Response({"count": Count}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Some exception occured while getting total number of tasks Exception: {e}")
            return Response({"error": "Not able to get count"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# %%%%%%%%%%%%%%% TEMPLATE SECTION %%%%%%%%%%%%%%%%%%%%

def list_tasks_page(request):
    return render(request, "todo/list_task.html")

def add_task_page(request):
    return render(request, "todo/add_task.html")