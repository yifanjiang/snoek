from activities.models import *
from django.contrib.auth.models import User

class Voter():

    def __init__(self, uid):
        self.id = uid
        self.user = User.objects.get(id = uid)

    def getAnswerOfQuestion(self, q):
        try:
            return Answer.objects.get(question=q.id, user=self.id)
        except Answer.DoesNotExist:
            return False

    def hasVoted(self, q):
    # return Boolean
    # test if the voter has voted the specific question.
        pass

