from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    my_user_data = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields=[
            'id',
            'my_user_data',
            'title',
            'date_start',
            'date_end', 
            'location',
            'description',
            'status'
        ]
    
    def get_my_user_data(self, obj):
        return {"username": obj.user.username}
