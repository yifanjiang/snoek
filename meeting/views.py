# Create your views here.
#import os, datetime
import datetime

#from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
#from django.http import HttpResponse
from django.http import HttpResponseServerError
#from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from snoek.meeting.models import *
from snoek.meeting.MeetingDiagram import *
from snoek import settings

# Private Function
############
def validation_check(event):
    es=event.start_time
    ee=event.end_time

    events = Event.objects.filter(meeting_room=event.meeting_room)

    for ev in events:
	    if (es.__ge__(ev.start_time) and es.__lt__(ev.end_time)) or \
                (ee.__gt__(ev.start_time) and ee.__le__(ev.end_time)):
                break
    else:
        return True

    #if break
    return False

# First Page
############
def index(request):
    # Show the basic functions
    return render_to_response('meeting/index.html',{'user':request.user,'settings':settings})

# Details function
############
@login_required
def show_meeting(request):
    # Show all meetings that need to attend
    meetings = Event.objects.filter(audience=request.user).order_by("meeting_room")
    return render_to_response('meeting/usermeeting.html',{'user':request.user,'settings':settings,'meetings':meetings})

@login_required
def show_event(request):
    # Show all meetings that hold by the login user
    events = Event.objects.filter(holder=request.user).order_by("meeting_room")
    return render_to_response('meeting/userevent.html',{'user':request.user,'settings':settings,'events':events})

@login_required
def new_event(request):
    alluser=User.objects.all()
    return render_to_response('meeting/new_event.html',{'user':request.user,'settings':settings,'alluser':alluser})

@login_required
def del_event(request,e_id):
    event=Event.objects.get(id=e_id)
    event.delete()
    events = Event.objects.filter(holder=request.user).order_by("meeting_room")
    return render_to_response('meeting/userevent.html',{'user':request.user,'settings':settings,'events':events})

@login_required
def set_event(request):
    # Book a meeting room and create a new event
    if request.method!='POST':
        return HttpResponseServerError("Should using 'POST' method in the 'form' of HTML,which using '%s'."
				% (request.method))
    #Save new event
    p = request.POST
    if p['roomno'] == "":
        return HttpResponseServerError("Please select a meeting room.")

    pdate_list=p['date'].split('-')
    pdate_year=int(pdate_list[0])
    pdate_month=int(pdate_list[1])
    pdate_day=int(pdate_list[2])

    pdate=datetime.date(pdate_year,pdate_month,pdate_day)
    key=pdate.isoformat()+u"   Room: "+p['roomno']

    room = MeetingRoom(dayroom=key, date=pdate, room_no=p['roomno'])

    stime_list=p['starttime'].split(':')
    stime_hour=int(stime_list[0])
    stime_min=int(stime_list[1])
    if len(stime_list)==3:
        stime_sec=int(stime_list[2])
    else:
        stime_sec=0
    starttime=datetime.time(stime_hour,stime_min,stime_sec)

    etime_list=p['endtime'].split(':')
    etime_hour=int(etime_list[0])
    etime_min=int(etime_list[1])
    if len(etime_list)==3:
        etime_sec=int(etime_list[2])
    else:
        etime_sec=0

    #Should eliminate the time after offwork
    if settings.ENDTIME == etime_hour:
        etime_min=0
        etime_sec=0
    endtime=datetime.time(etime_hour,etime_min,etime_sec)

    newevent = Event(meeting_room=room, start_time=starttime, end_time=endtime,
			holder=User.objects.get(username=p['holder']),purpose=p['purpose'])

    #Show error if the event time confilct with exist one
    if not validation_check(newevent):
        return HttpResponseServerError("Confilct with exist event,should change another room or time.")

    room.save()
    newevent.save()

    ulist = p.getlist('participant')
    for u in ulist:
        newevent.audience.add(User.objects.get(username=u))
    newevent.save()

    #Show all events
    events = Event.objects.filter(holder=request.user).order_by("meeting_room")
    return render_to_response('meeting/userevent.html',{'user':request.user,'settings':settings,'events':events})

def get_status(request):
    # Show meeting room status of today and get requirement
    return render_to_response('meeting/status.html',{'user':request.user,'settings':settings})

def show_status(request):
    # Show all meeting room status
    if request.method!='GET':
        return HttpResponseServerError("Should using 'GET' method in the 'form' of HTML,which using '%s'."
				% (request.method))
    g = request.GET

    # Get the date and roomno
    diagram_list=[]

    if g['date'] == '' and g['roomno'] == '':
        #Empty input,all rooms in today are default.
        today = datetime.date.today()
        for no in settings.ROOMNO:
            key = today.isoformat()+u"   Room: "+unicode(no)
            room=MeetingRoom(dayroom=key,date=today,room_no=no)

	    dia=MeetingDiagram(room)

            dia.setEvents()
            diagram_list.append(dia)

    elif g['date'] == '':
        #Only input roomno
        today = datetime.date.today()
	#Show 3 days from today
        for increasement in range(0,3):
            temday = today+datetime.timedelta(increasement)
            key = temday.isoformat()+u"   Room: "+g['roomno']
            room=MeetingRoom(dayroom=key,date=temday,room_no=g['roomno'])

            dia=MeetingDiagram(room)

            dia.setEvents()
            diagram_list.append(dia)

    elif g['roomno'] == '':
        #Only input date
        for no in settings.ROOMNO:
            gdate_list=g['date'].split('-')
            gdate_year=int(gdate_list[0])
            gdate_month=int(gdate_list[1])
            gdate_day=int(gdate_list[2])

            gdate=datetime.date(gdate_year,gdate_month,gdate_day)
            key=gdate.isoformat()+u"   Room: "+unicode(no)

	    room=MeetingRoom(dayroom=key,date=gdate,room_no=no)

	    dia=MeetingDiagram(room)

            dia.setEvents()
            diagram_list.append(dia)
    else:
        #Input both date and roomno
        gdate_list=g['date'].split('-')
        gdate_year=int(gdate_list[0])
        gdate_month=int(gdate_list[1])
        gdate_day=int(gdate_list[2])

        gdate=datetime.date(gdate_year,gdate_month,gdate_day)
        key=gdate.isoformat()+u"   Room: "+g['roomno']

	room= MeetingRoom(dayroom=key,date=gdate,room_no=g['roomno'])
	dia=MeetingDiagram(room)

        dia.setEvents()
        diagram_list.append(dia)

    return render_to_response('meeting/showdiagram.html',{'user':request.user,'settings':settings,'diagrams':diagram_list})
