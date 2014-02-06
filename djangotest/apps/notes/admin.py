from django.contrib import admin
from notes.models import Notes, Book

class NotesAdmin(admin.ModelAdmin):

    """
    Create admin interface for text notes.
    """
    
    list_display = ("pk", "id", "title", "text")

class NotesInline(admin.StackedInline):
    model = Notes.books.through
    extra = 0

class BookAdmin(admin.ModelAdmin):

    """
    Create admin interface for books.
    """
    
    list_display = ("title", )
    inlines = [NotesInline,]
    exclude = ('notes',)



admin.site.register(Notes, NotesAdmin)
admin.site.register(Book, BookAdmin)