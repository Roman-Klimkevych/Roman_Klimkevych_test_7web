from django.views.generic import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from notes.models import Notes
from notes.forms import AddNoteForm
from django.http import *
from django.template.loader import render_to_string
import json

class NotesDisplay(FormMixin, ListView):
    
    """
    Display text notes and form when the request is get.
    """
    
    queryset = Notes.objects.order_by('-id')    
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        """ Add form to the context data."""
        context = super(NotesDisplay, self).get_context_data(**kwargs)
        context['form'] = AddNoteForm()
        return context

class NotesFormProcessor(MultipleObjectMixin, FormView):
    
    """
    Display text notes and form when the request is post.
    """
    queryset = Notes
    
    def post(self, request, *args, **kwargs):
        """ Check wether the form is valid or not."""
        form = AddNoteForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """ 
        Perform actions for valid form.

        Save note to the database. 
        Render latest note, total notes count and sucess message.
        Return HttpResponse.

        """
        
        note_id = self.queryset.objects.latest('id').id + 1
        new_note = form.cleaned_data['note']
        added_note = Notes(title="Note_" + str(note_id), text=new_note)
        added_note.save()
        
        latest_note = self.queryset.objects.latest('id')
        title = latest_note.title
        text = latest_note.text
        render = render_to_string('ajax_note.html', {'title': title, "text": text})
        count = self.queryset.objects.count()
        message = "Your text note has been successfully added!!!"
        
        response_dict = {}
        response_dict.update({'new_note': render, 'count': count, 'message': message })
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    
    def form_invalid(self, form):
        """ 
        Perform actions for invalid form.

        Render error message.
        Return HttpResponse.

        """
        error = form['note'].errors
        response_dict = {}
        response_dict.update({'errors': error })
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')

class NotesView(View):
    
    """
    Receive request from reverse('text_notes') URL.
    """
    
    def get(self, request, *args, **kwargs):
        """ Return NotesDisplay if the request is get."""
        view = NotesDisplay.as_view()
        return view(request, *args, **kwargs)

class AjaxView(View):
    
    """
    Receive request from reverse('ajax_notes') URL.
    """

    def post(self, request, *args, **kwargs):
        """ Return NotesFormProcessor if the request is post."""
        view = NotesFormProcessor.as_view()
        return view(request, *args, **kwargs)
