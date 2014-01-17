from django.http import HttpResponse
from django.views.generic import ListView
from notes.models import Notes

class NotesView(ListView):
	model = Notes
	context_object_name = "notes"

	def home(self, *args, **kwargs):
		return HttpResponse()	