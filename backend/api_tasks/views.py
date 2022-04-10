from urllib import request
from rest_framework import generics, permissions, authentication
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsCustomerPermission
from api_tasks.mixins import UserQuerySetMixin


class TaskCreateAPIView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [IsCustomerPermission]

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        if description is None:
            description = title
        serializer.save(user=self.request.user, description=description)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        return qs.filter(user=request.user)


class TaskDetailAPIView(UserQuerySetMixin, generics.RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class TaskUpdateAPIView(UserQuerySetMixin, generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.description:
            instance.description = instance.title 

class TaskDeleteAPIView(UserQuerySetMixin, generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'pk'
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(serl, instance):
        super().perform_destroy(instance)

class TaskListAPIView(UserQuerySetMixin, generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]

class SearchListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]


    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        q = self.request.GET.get('q')
        results = Task.objects.none()
        if q is not  None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(q, user=user)
        return results 