from django.contrib import admin
from notes.models import Notes

class NotesAdmin(admin.ModelAdmin):
    list_display = ("title", "text")
    
admin.site.register(Notes, NotesAdmin)