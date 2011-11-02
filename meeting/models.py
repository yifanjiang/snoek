from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class MeetingRoom(models.Model):
    dayroom = models.CharField(max_length=20, primary_key=True)
    date = models.DateField(help_text="Required. Show like year-month-day. eg,2011-10-11")
    room_no = models.IntegerField(help_text="Required.")

    def __unicode__(self):
        return self.dayroom

    class Meta:
        ordering = ['-date']

class Event(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom)
    start_time = models.TimeField()
    end_time = models.TimeField()
    holder = models.ForeignKey(User, related_name="holder")
    audience = models.ManyToManyField(User, related_name="audience")
    purpose = models.CharField(max_length=200)

    def __unicode__(self):
        return unicode(self.holder)+" "+unicode(self.meeting_room.date)

    def getAllAudience(self):
        return self.audience.all()

    getAud=property(getAllAudience)
