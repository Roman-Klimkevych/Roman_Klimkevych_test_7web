from django.contrib import admin
from notes.models import Notes

class NotesAdmin(admin.ModelAdmin):

    """
    Create admin interface for text notes
    """
    
    list_display = ("title", "text")
    
admin.site.register(Notes, NotesAdmin)