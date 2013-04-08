from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Activity(models.Model):

    summary = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()
    category = models.CharField(max_length=30)
    user = models.ForeignKey(User)
    created_datetime = models.DateTimeField(auto_now_add=True, null=True)

    def getAllAnswers(self, voter=""):
        # voter is a User object
        result = []
        if voter == "":
            for v in self.vote_set.all():
                for q in v.question_set.all():
                    for a in q.answer_set.all():
                        result.append(a)
        else:
            for v in self.vote_set.all():
                for q in v.question_set.all():
                    for a in q.answer_set.filter(user = voter):
                        result.append(a)
        return result

    def getVoteNumber(self):
        
        first_vote = self.vote_set.all()[0]
        return Answer.objects.filter(question__vote=first_vote).count()

    total_votes = property(getVoteNumber)

class Vote(models.Model):

    summary = models.CharField(max_length=100)
    description = models.TextField()
    activity = models.ForeignKey(Activity)

    def getAllQuestions(self):
        return Question.objects.filter(vote = self.id)

    def getAllAnswersCount(self):
        num = 0
        for q in self.question_set.all():
            num = num + q.answer_set.count()
        return num

    questions = property(getAllQuestions)
    answerscount = property(getAllAnswersCount)

class Question(models.Model):

    vote = models.ForeignKey(Vote)
    content = models.CharField(max_length=100)
    hyperlink = models.CharField(max_length=1000)

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
