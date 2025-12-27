from rest_framework import serializers
from datetime import datetime

def current_ts_ms():
    int(datetime.now().timestamp()*1000)

class TaskSerializer(serializers.Serializer):
    title       = serializers.CharField(max_length=255, required=True)
    description = serializers.CharField(required=False)
    status      = serializers.ChoiceField(choices=["pending", "completed"], required=False, default="pending")
    due_date    = serializers.DateTimeField(required=False, allow_null=True)

    def validate_due_date(self, value):
        if value is None:
            return current_ts_ms()
        return value
