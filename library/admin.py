from django.contrib import admin
from library.models import Book, BookReader
class BookAdmin(admin.ModelAdmin):
    pass
admin.site.register(Book)

class BookReaderAdmin(admin.ModelAdmin):
    pass
admin.site.register(BookReader,BookReaderAdmin)
