# Create your views here.
from django.http import HttpResponseRedirect,HttpResponseForbidden,HttpResponse
from django.forms import ModelForm
from django.shortcuts import render_to_response,get_object_or_404
from django.contrib.auth.decorators import login_required
from library.models import *
from django.core.context_processors import csrf
import urllib2
from django.conf import settings
from xml.dom import minidom
import cStringIO
from django.core.files.base import ContentFile
from django.views.generic.list_detail import object_list
from django.forms import ModelForm
from django.template import RequestContext
from django.core.urlresolvers import reverse
from getBookInfo.tasks import getBookInfo as task_getbookinfo


#def search(request,)

#def lent(reqeuest,)

def bookreader_detail(request,object_id):
    reader=get_object_or_404(BookReader,pk=object_id)
    queryset=reader.book_set.all()
    count=len(queryset)
    return object_list(request,
                         queryset=queryset,
                         extra_context={'reader':reader,'count':count},
                         template_object_name='book',
                         template_name='library/bookreader_detail.html',
                         )
                        
class BookForm(ModelForm):
    class Meta:
        model=Book

def update(request,object_id):
    if not request.is_ajax():
        book=get_object_or_404(Book,pk=object_id)
        books = Book.objects.all()
        return object_list(request,
                            queryset=books,
                            template_object_name='book',
                            template_name = 'library/book_list.html')

    book = Book.objects.get(pk=object_id)
    if request.method == "POST":
           book_form = BookForm(request.POST, request.FILES, instance = book)
           if book_form.is_valid():
               book = book_form.save()
               return render_to_response("library/success.html",{"book":book})
           return render_to_response("library/book_detail_edit.html",
                    {"form":book_form, "pk":object_id},
                    context_instance=RequestContext(request))
    else:
        if request.user.is_staff:
            template = "library/book_detail_edit.html"
            book_form = BookForm(instance = book)
            return render_to_response(template,
                    {"form":book_form, "pk":object_id},
                    context_instance=RequestContext(request))
        else:
            template = "library/book_detail_view.html"
            return render_to_response(template,
                    {"book":book, "pk":object_id},
                    context_instance=RequestContext(request))


@login_required
def create(request):
    if request.method == "POST":
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            new_book = book_form.save()
            task_getbookinfo.delay(new_book.pk)
            return HttpResponseRedirect(reverse("library_book_list"))
    else:
        book_form = BookForm()
    return render_to_response("library/book_create.html",{"form":book_form},
            context_instance=RequestContext(request))

        

@login_required
def delete(request, object_id):
    book=Book.objects.get(pk=object_id)
    if book.bookCover:
        book.bookCover.delete()
    book.delete()
    return render_to_response("library/success.html")
    #return HttpResponseRedirect(reverse("library_book_list"));



def getBookInfo(request, object_id):
    book=get_object_or_404(Book,pk=object_id)
    task_getbookinfo(book.pk)
    return HttpResponseRedirect(book.get_absolute_url())
