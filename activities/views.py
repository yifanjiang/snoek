# Create your views here.
import os, datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, TableColumnProperties, Map
from odf.number import NumberStyle, CurrencyStyle, CurrencySymbol,  Number,  Text
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell

from snoek.activities.models import *
from snoek import settings
# from snoek.activities.models import Vote
# from snoek.activities.models import Answer
# from snoek.activities.models import Question

from snoek.activities.VoteTable import VoteTable

# First Page
############

def index(request, category = None):
    # Controller interface: View an activity
    # input: An activity id
    # return: Rendering an activity page

    user = request.user
    if category:                        # Show activities in a specific category.
        pass
    else:
        return render_to_response('index.html', {'user': user,
                                                 'settings': settings,
                                                 'avt': reversed(list(Activity.objects.all()))})

# ACTIVITIES
############

def view_activity(request, a_id):
    # Controller interface: View an activity
    # input: An activity id
    # return: Rendering an activity page

    user = request.user    

    avt = Activity.objects.get(id = a_id)
    votes = Vote.objects.filter(activity = a_id)
    vote_tables = []

    # Generate all 1D table
    for v in votes:
        vote_tables.append({'vote': v, 'table': VoteTable(v.id)})
    
    # Generate all possible 2D table
    for i in range(len(votes)):
        for j in range(i+1, len(votes)):
            vote_tables.append({'vote': '', 'table': VoteTable(votes[i].id, votes[j].id)})
    #debug
    #for v in votes:
    #    for q in list(v.question_set.all()):
    #        print q.content
        #for q in list(v.question_set):
        #    print q.content

    return render_to_response('show_activity.html', {'avt': avt,
                                                     'votes': votes,
                                                     'vote_tables': vote_tables,
                                                     'user':user,
                                                     'settings': settings,
                                                     'has_voted': _hasVoted(user, avt),
                                                     'is_expired': _isExpired(avt),
                                                     'settings': settings
                                                     })

@login_required
def view_create_activity(request,category):
    user=request.user
    return render_to_response('new_activity.html',{'user':user,
                                                   'category':category,
                                                   'settings':settings,
						   'avt':reversed(list(Activity.objects.all()))})

@login_required
def view_update_activity(request,aid):
    p=Activity.objects.get(id=aid)
    vote=list(Vote.objects.filter(activity=p))
    votetable=[]
    for v in vote:
        q=list(Question.objects.filter(vote=v))
        if len(q)<5:
           q=q+['']*(5-len(q))
        votetable.append([v,q])
    if len(votetable)<2:
       votetable=votetable+['']*(2-len(votetable))
    return render_to_response('edit_activity.html',{'user':request.user,
                                                    'settings':settings,
                                                    'avt':p, 
                                                    'vq':votetable,
                                                    'ql':range(1,6)})


@login_required
def create_activity(request):
    if request.method=='POST':
       s=request.POST
    datelist=s['deadline'].split('-')
    year=int(datelist[0])
    mon=int(datelist[1])
    day=int(datelist[2])
    p=Activity(user=request.user,summary=s['summary'],description=s['description'],deadline=datetime.date(year,mon,day),category=s['category'])
    p.save()
    return render_to_response('new_votes.html',{'user':request.user,
                                                'settings':settings,
                                                'act':p})


@login_required
def save_vote_in_activity(request,aid):
    if request.method=='POST':
       s=request.POST
    act=Activity.objects.get(id=aid)
    if s['v1s']!='':
       vote1=Vote(summary=s['v1s'],description=s['v1d'],activity=act)
       vote1.save()
       for content in ['v1q1','v1q2','v1q3','v1q4','v1q5']:
           if s[content]!='':
              Question(content=s[content],vote=vote1).save()
    if s['v2s']!='':
       vote2=Vote(summary=s['v2s'],description=s['v2d'],activity=act)
       vote2.save()
       for content in ['v2q1','v2q2','v2q3','v2q4','v2q5']:
           if s[content]!='':       
              Question(content=s[content],vote=vote2).save()
    return HttpResponseRedirect('/')
  #  return render_to_response('index.html', {'user': request.user,
   #                                          'settings': settings,
    #                                         'avt': reversed(list(Activity.objects.all()))})

@login_required
def delt_activity(request,aid):

    p=Activity.objects.get(id=aid)

    if request.user == p.user:    
        for v in Vote.objects.filter(activity=p):
            for a in Question.objects.filter(vote=v):
                Answer.objects.filter(question=a).delete()
            Question.objects.filter(vote=v).delete()
        Vote.objects.filter(activity=p).delete()
        p.delete()
    else:
        return False
    return HttpResponseRedirect('/')
   
@login_required
def update_activity(request,aid):
    if request.method=='POST':
       s=request.POST
    dl=s['deadline'].split('-')
    p=Activity(id=aid,user=request.user,summary=s['summary'],description=s['description'],deadline=datetime.date(int(dl[0]),int(dl[1]),int(dl[2])),category=s['category'])
    p.save()
    lenvote=len(Vote.objects.filter(activity=p))    
    for v in Vote.objects.filter(activity=p):
        if s[str(v.id)]=='':
           for q in Question.objects.filter(vote=v):
               Answer.objects.filter(question=q).delete()
               q.delete()
           v.delete()
        else:
           v.summary=s[str(v.id)]
           v.description=s['d'+str(v.id)]
           v.save()
           lenq=len(Question.objects.filter(vote=v))
           for q in Question.objects.filter(vote=v):
               if s[str(v.id)+'-'+str(q.id)]=="":  
                  Answer.objects.filter(question=q).delete()
                  q.delete()
               elif s[str(v.id)+'-'+str(q.id)]!=q.content:
                  Answer.objects.filter(question=q).delete()
                  q.content=s[str(v.id)+'-'+str(q.id)]
                  q.save()
               else:
                  pass
           if lenq<5:
              for i in range(lenq+1,6):
                  if s[str(v.id)+'p'+str(i)]!="":
                     Question(content=s[str(v.id)+'p'+str(i)],vote=v).save()
    if lenvote<2:
        for i in range(lenvote+1,3):
            if s['v'+str(i)]!='':
               vn=Vote(summary=s['v'+str(i)],description=s['vd'+str(i)],activity=p)
               vn.save()
               for j in range(1,6):
                   if s['v'+str(i)+'p'+str(j)]!='':
                      Question(content=s['v'+str(i)+'p'+str(j)],vote=vn).save()
    return HttpResponseRedirect('/')

def download_activity(request, a_id):
    # Controller interface: Download an activity
    # input: An activity id
    # return: Rendering an ods file for download
    avt = Activity.objects.get(id = a_id)
    filename = 'snoek-activity-' + str(avt.id) + '-' + str(avt.summary)
    votes = Vote.objects.filter(activity = a_id)

    odf_table_list = []

    # Generate all 1D table
    for v in votes:
        odf_table_list.append(_toODSTable(VoteTable(v.id)))
    
    # Generate all possible 2D table
    for i in range(len(votes)):
        for j in range(i+1, len(votes)):
            odf_table_list.append(_toODSTable(VoteTable(votes[i].id, votes[j].id)))

    f = _toODSFile(odf_table_list, filename)
    
    response = HttpResponse(f, mimetype='application/vnd.oasis.opendocument.spreadsheet')
    response['Content-Disposition'] = 'attachment;filename="%s"' % os.path.basename(f.name)
    return response

# VOTES
#######

def view_votes_by_all_users(request, a_id):
    # Controller interface: View an activity voting results by User
    # input: An activity id
    # return: Rendering an who vote for what table

    user = request.user
    avt = Activity.objects.get(id = a_id)
    vote_tables = []
    votes = Vote.objects.filter(activity = a_id)

    for v in votes:
        vt = VoteTable(v.id)
        vote_tables.append({'vote': v, 'table': vt})

    return render_to_response('whovotewhat.html', {'avt': avt, 'vote_tables': vote_tables, 'settings': settings, 'user':user})

@login_required
def take_vote(request, a_id):
    u_id = request.user.id

    for v in request.POST:
        q_id = request.POST[v]
        answer = Answer(question=Question.objects.get(pk=q_id), user=User.objects.get(pk=u_id))
        answer.save()

    return HttpResponseRedirect('/activity/' + a_id)

@login_required
def take_revote(request, a_id):

    u_id = request.user.id
    avt = Activity.objects.get(id = a_id)
    
    for a in avt.getAllAnswers(request.user):
        a.delete()

    for v in request.POST:
        q_id = request.POST[v]
        answer = Answer(question=Question.objects.get(pk=q_id), user=User.objects.get(pk=u_id))
        answer.save()        

    return HttpResponseRedirect('/activity/' + a_id)

@login_required
def del_vote(request, a_id):

    u_id = request.user.id
    avt = Activity.objects.get(id = a_id)

    for a in avt.getAllAnswers(request.user):
        a.delete()

    return HttpResponseRedirect('/activity/' + a_id)        
    
# Internal functions
####################

def _toODSFile(odf_table_list, filename):
    
    doc = OpenDocumentSpreadsheet()
    for t in odf_table_list:
        doc.spreadsheet.addElement(t)

    doc.save('/tmp/' + filename, True)
    return file('/tmp/' + filename + '.ods')

def _toODSTable(v_table):
    # generate an ods file to download
    # input: Object VoteTable
    # output: Object ods.table

    table= Table(name=v_table.title)

    row_head = v_table.row_head
    col_head = v_table.col_head
    table_body = v_table.table_body

    # Render column head if it is a 2D table
    if v_table.is2D():
        table.name = '2D'
        tr= TableRow()
        table.addElement(tr)
        td= TableCell()
        td.addElement(P(text='Head'))
        tr.addElement(td)                            
        for headcell in v_table.col_head:
            td= TableCell()
            td.addElement(P(text=headcell.content))
            tr.addElement(td)                    
    
    for cursorRow in v_table.table_with_row:
        tr= TableRow()
        table.addElement(tr)
        td= TableCell()
        td.addElement(P(text=cursorRow['row_head'].content))
        tr.addElement(td)                    

        for val in cursorRow['row_body']:
            td= TableCell()            
            td.addElement(P(text=val))
            tr.addElement(td)    

    #myFile= tempfile.TemporaryFile('/tmp/')
    #doc.save('/tmp/test', True)
    return table
    
# def _isValidForVote(usr, avt):
#     # return if votes in a activity is allowed

#     # TODO if activity is expired
#     if _isExpired(avt):
#         return False
    
#     # if user is invalid
#     for v in avt.vote_set.all():        
#         for q in v.question_set.all():
#             try:
#                 if q.answer_set.filter(user = usr):
#                     return False        # usr has voted
#                 else:
#                     continue
#             except TypeError:
#                 return False            # usr is anonymous
#     return True

def _hasVoted(usr, avt):

    # if user is invalid
    for v in avt.vote_set.all():        
        for q in v.question_set.all():
            try:
                if q.answer_set.filter(user = usr):
                    return True        # usr has voted
                else:
                    continue
            except TypeError:
                return True            # usr is anonymous
    return False

def _isExpired(avt):
    # return if activity is expired

    d = avt.deadline
    return datetime.datetime(d.year, d.month, d.day) <= datetime.datetime.now()

