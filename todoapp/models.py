from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
	item = models.CharField(max_length=100)
	priority = models.IntegerField(default=5)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.item}'
