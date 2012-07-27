from celery.task import task
from xml.dom import minidom
import cStringIO
import urllib2
from library.models import *
from django.core.files.base import ContentFile

@task
def getBookInfo(object_id):
    appkey='0264189fddab652f072c49df99022f8d'
    book=Book.objects.get(pk=object_id)
    isbn=book.isbn
    path="http://api.douban.com/book/subject/isbn/"+isbn+"?appkey="+appkey
    try:
        conn=urllib2.urlopen(path)
        req=conn.read()
    except Exception:
        print "download info error"
    xmldoc=minidom.parse(cStringIO.StringIO(req))
    patent=xmldoc.firstChild
    #title
    book.title=patent.getElementsByTagName('title')[0].firstChild.data.strip().encode('utf8')
    #summary
    book.briefIntro =patent.getElementsByTagName('summary')[0].firstChild.data.strip().encode('utf8')
    #img

    for i in patent.getElementsByTagName('link'):
        if i.getAttribute('rel')==u'image':
            img=i.getAttribute('href')
    #get large img
    img=img.replace('spic','lpic')
    result=downloadImage(img)
    if result:
        book.bookCover.save(result[0],ContentFile(result[1]),save=True)
        book.save()
    else:
        print "download info error"



def downloadImage(img):
    tries=1
    while tries < 3:
        try:
            conn=urllib2.urlopen(img)
            imgData=conn.read()
            filename=img.split('/')[-1]
            return (filename,imgData)
        except:
            tries+=1
    return None
