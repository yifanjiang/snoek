from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Activity(models.Model):

    summary = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    category = models.CharField(max_length=30)
    user = models.ForeignKey(User)

class Vote(models.Model):

    summary = models.CharField(max_length=100)    
    description = models.TextField()
    activity = models.ForeignKey(Activity)

    def getAllQuestions(self):
        return Question.objects.filter(vote = self.id)

    questions = property(getAllQuestions)    

class Question(models.Model):

    content = models.CharField(max_length=100)    
    vote = models.ForeignKey(Vote)

    def getAnswersNumber(self):
        return len(Answer.objects.filter(question = self.id))
    
    def getAllAnswers(self):
        return Answer.objects.filter(question = self.id)

    answernumber = property(getAnswersNumber)
    answers = property(getAllAnswers)

class Answer(models.Model):
    
    question = models.ForeignKey(Question)
    user = models.ForeignKey(User)
    
    def getAllVoters(self):
        return User.objects.filter(id = user)
    
    voters = property(getAllVoters)
