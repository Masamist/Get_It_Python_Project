from time import time
from django.db import models
from django.forms import CharField
from django.db.models import Sum

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50)
    whatHeading = models.CharField(max_length=150, default="wHeading here...")
    whatDescription = models.TextField(max_length=500, default="wDescription here...")
    howHeading = models.CharField(max_length=150, default="hHeading here...")
    howDescription = models.TextField(max_length=500, default="hDescription here...")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    
    template_user_result = models.SmallIntegerField(default=0)
    
    def __str__(self):
        return self.name

    @property
    def count_questions(self):
        return Question.objects.filter(content__topic__course = self).count()


class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete= models.CASCADE)
    name = models.CharField(max_length=50, default="name here...")
    intro = models.TextField(max_length=500, default="intro here...")

    def __str__(self):
        str = self.course.name + ", " + self.name
        return str
    
    @property
    def count_questions(self):
        return Question.objects.filter(content__topic = self).count()

class Content(models.Model):
    topic = models.ForeignKey(Topic, on_delete= models.CASCADE, default=4)
    name = models.CharField(max_length=50, default="name here...")
    explanation = models.TextField(max_length=500, default="explanation here...")
    example = models.TextField(max_length=500, default="example here...")
    minutesToComplete = models.SmallIntegerField(default=8)
    template_user_result = models.SmallIntegerField(default=0)

    def __str__(self):
        str = self.topic.course.name + ", " + self.topic.name + ", " + self.name
        return str

    @property
    def count_questions(self):
        return Question.objects.filter(content = self).count()


class Question(models.Model):
    content = models.ForeignKey(Content, on_delete= models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.BooleanField()

    def __str__(self):
        str = self.content.topic.course.name + ", " + self.content.topic.name + ", " + self.content.name + ", " + self.question
        return str