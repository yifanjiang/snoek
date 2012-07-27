from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from library.models import *

book_info={'queryset':Book.objects.all(),'template_object_name':'book'}
reader_info={'queryset':BookReader.objects.all(),'template_object_name':'bookreader'}


urlpatterns= patterns('',
                      url(r'^$',
                          object_list,
                          dict(book_info,paginate_by=8),
                          name='library_book_list'),

                      url(r'^(?P<object_id>\d+)/$',
                          'library.views.update',
                          name='library_book_detail'),

                      url(r'^delete/(?P<object_id>\d+)/$',
                          'library.views.delete',
                          name='library_book_delete'),

                      url(r'^create/$',
                          'library.views.create',
                            name='library_book_create'),

                      url(r'^getBookInfo/(?P<object_id>\d+)/$',
                          'library.views.getBookInfo',
                          name='library_get_bookinfo'),

                      url(r'^readers/$',
                          object_list,
                          dict(reader_info,paginate_by=20),
                          name='library_readers'),

                      url(r'^reader/(?P<object_id>\d+)/$',
                          'library.views.bookreader_detail',
                          name='library_reader'),
                      )
