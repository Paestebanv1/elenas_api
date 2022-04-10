from django.db import models
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL

# Class to verify if the task is public and find a string into the description
class TaskQuerySet(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, query, user=None):
        lookup = Q(description__icontains=query)
        qs = self.is_public().filter(lookup)
        if user is not None:
            qs2 = self.filter(user=user).filter(lookup)
            qs = (qs | qs2).distinct()
        return qs


class TaskManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return TaskQuerySet(self.model, using=self._db)

    def search(self, query, user=None):
        return self.get_queryset.search(query)


# Create your models here.
class Task(models.Model):
    status_options = [
        ('CP', 'Complete'),
        ('IC', 'Incomplete'),
        ('IP', 'In progress'),
        ('CD', 'Canceled'),
        ('PD', 'Pending'),
        ('RM', 'Removed'),
    ]
    title = models.CharField(max_length=120)
    date_start = models.DateTimeField(null=True)
    date_end = models.DateTimeField(null=True)
    location = models.CharField(max_length=120, null=True)
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    public = models.BooleanField(default=True)
    status = models.CharField(
        max_length=2,
        choices=status_options,
        default='PD'
    )
    objects = TaskManager() 
    
