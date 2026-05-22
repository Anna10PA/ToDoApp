from django.db import models
from datetime import datetime


class task(models.Model):
    tasks = models.CharField()
    email = models.CharField()
    add_time = models.DateTimeField(auto_now_add=True)
    completed_time = models.DateTimeField(auto_now_add=False)
    deadline_time = models.DateTimeField(auto_now_add=False)
    deleted_time = models.CharField(null=True)
    category = models.CharField(default='default')


class delt(models.Model):
    tasks = models.CharField()
    email = models.CharField()
    add_time = models.CharField(null=True)
    completed_time = models.CharField(null=True)
    deadline_time = models.CharField(null=True)
    deleted_time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(default='default')


class category(models.Model):
    category = models.CharField(default='default')
    email = models.CharField()