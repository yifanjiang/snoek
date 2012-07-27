from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.db.models import permalink

# Create your models here.
class BookReader(models.Model):
    user=models.ForeignKey(User,unique=True)
    def __unicode__(self):
        return self.user.username
    @permalink
    def get_absolute_url(self):
        return ('library_reader',(),{'object_id':self.pk})

class Book(models.Model):
    title=models.CharField('title',max_length=100,unique=True)
    isbn=models.CharField('isbn',max_length=100,unique=True)
    tagNumber=models.CharField('tag',max_length=100,unique=True)
    borrower=models.ForeignKey (BookReader,null=True,blank=True)
    bookCover=models.ImageField('Cover',upload_to='upload_images/',blank=True)
    joinInDate=models.DateTimeField('joinInDate',auto_now_add=True)
    briefIntro=models.TextField('introduction',blank=True)
    @permalink
    def get_absolute_url(self):
        return ('library_book_detail',(),{'object_id':self.pk})

    def __unicode__(self):
        return self.title

