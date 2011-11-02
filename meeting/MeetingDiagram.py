from snoek.meeting.models import *
from snoek.settings import STARTTIME,ENDTIME,UNITCOLOR
from django.contrib.auth.models import User

class MeetingDiagram(object):
    '''One day meeting room diagram.'''
    def __init__(self,MeetingRoom):
	#init all units. time,color,event(holder: time,purpose)
        self.units = []
        self.meetingroom = MeetingRoom
        for i in range(STARTTIME,ENDTIME):
            self.units.append([unicode(i)+":00-"+unicode(i+1)+":00",UNITCOLOR[False],[]])

    def setEvents(self):
        Events=Event.objects.filter(meeting_room=self.meetingroom).order_by('start_time')
        for event in Events:
            #Set unit flag
            self.stime = event.start_time
            self.etime = event.end_time
	    if self.stime.hour == self.etime.hour:
                self.units[self.stime.hour-STARTTIME][1]=UNITCOLOR[True]
            else:
                if self.etime.minute == 0 and self.etime.second == 0:
                    for index in range(self.stime.hour-STARTTIME, self.etime.hour-STARTTIME):
                        self.units[index][1]=UNITCOLOR[True]
                else:
                    for index in range(self.stime.hour-STARTTIME, self.etime.hour-STARTTIME+1):
                        self.units[index][1]=UNITCOLOR[True]

            #Set unit event info
            self.units[self.stime.hour-STARTTIME][2].append((event.holder.username+": "+\
                self.stime.isoformat()+"--"+self.etime.isoformat(),event.purpose))
        return True
