from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('auth/', obtain_auth_token),
    path('', views.TaskCreateAPIView.as_view(), name="create_tasks"),
    path('list/', views.TaskListAPIView.as_view(), name="list_tasks"),
    path('<int:pk>/update', views.TaskUpdateAPIView.as_view(), name="update_tasks"),
    path('<int:pk>/delete', views.TaskDeleteAPIView.as_view(), name="delete_tasks"),
    path('search/', views.SearchListView.as_view(), name='search_tasks'),
    path('<int:pk>/', views.TaskDetailAPIView.as_view(), name="detail_tasks")
]
