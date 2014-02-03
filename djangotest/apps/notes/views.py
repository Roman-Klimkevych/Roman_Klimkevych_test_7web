from django.views.generic import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from notes.models import Notes
from notes.forms import AddNoteForm
from django.contrib import messages
from django.core.urlresolvers import reverse
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
    Display text notes and form when the request is post and not Ajax
    """
    
    queryset = Notes.objects.order_by('-id')
    form_class = AddNoteForm
    context_object_name = 'notes'
    template_name = 'notes/notes_list.html'

    def post(self, request, *args, **kwargs):
        """ Check wether the form is valid or not"""
        form = AddNoteForm(request.POST, request.FILES)
        self.object_list = self.get_queryset()
        if form.is_valid():
            messages.success(request, "Your text note has been successfully added!!!")
            return self.form_valid(form)
        else:
            return super(NotesFormProcessor, self).form_invalid(form)

    def form_valid(self, form):
        """ Save note to the database when the form is valid"""
        note_id = Notes.objects.latest('id').id + 1
        new_note = form.cleaned_data['note']
        new_image = form.cleaned_data['image']
        added_note = Notes(title="Note_" + str(note_id), text=new_note, image=new_image)
        added_note.save()
        return super(NotesFormProcessor, self).form_valid(form)

    def get_success_url(self):
        """ Return URL to redirect when the form is valid"""
        return reverse('text_notes')

class AjaxFormProcessor(MultipleObjectMixin, FormView):
    
    """
    Display text notes and form posted by ajax.
    """
    queryset = Notes
    
    def post(self, request, *args, **kwargs):
        """ Check wether the form is valid or not."""
        form = AddNoteForm(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form,request)
        else:
            return self.form_invalid(form, request)

    def form_valid(self, form, request):
        """ 
        Perform actions for valid form.

        Save note to the database. 
        Render latest note, total notes count and sucess message.
        Return HttpResponse.

        """
        
        note_id = self.queryset.objects.latest('id').id + 1
        new_note = form.cleaned_data['note']
        new_image = form.cleaned_data['image']  # 
        added_note = Notes(title="Note_" + str(note_id), text=new_note, image=new_image)
        added_note.save()
        
        latest_note = self.queryset.objects.latest('id')
        title = latest_note.title
        text = latest_note.text
        image = latest_note.image
        render = render_to_string('ajax_note.html', {'title': title, 'text': text, 'image': image})
        count = self.queryset.objects.count()
        message = "Your text note has been successfully added!!!"
        
        response_dict = {}
        response_dict.update({'new_note': render, 'count': count, 'message': message })
        return HttpResponse(json.dumps(response_dict), content_type='application/javascript')
    
    def form_invalid(self, form, request):
        """ 
        Perform actions for invalid form.

        Render error message.
        Return HttpResponse.

        """
        error_note = form['note'].errors
        error_image = form['image'].errors
        response_dict = {}
        response_dict.update({'error_note': error_note, 'error_image': error_image })
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
        """ Check if the request is ajax and return view to process form."""
        if request.is_ajax():
            view = AjaxFormProcessor.as_view()
        else:
            view = NotesFormProcessor.as_view()
        return view(request, *args, **kwargs)

from django.template import loader, Context, RequestContext
from django.shortcuts import render_to_response
from random import choice

class WidgetView(ListView):
    
    """
    Widget to display random text note.
    """
    
    queryset = Notes
    
    def get(self, request, color="blue"):
        color_dict = {
            "blue": "panel-info",
            "green": "panel-success",
            "yellow": "panel-warning",
            "red": "panel-danger"
            }
        notes = self.queryset.objects.all().values_list("id", flat=True)
        random_id = choice(notes)
        note = self.queryset.objects.get(id=random_id)
        t = loader.get_template('widget_content.html')
        c = Context({'note' : note, 'class': color_dict[color]})
        context = {"widget_content" : t.render(c)}
        return render_to_response("widget.html", context, context_instance=RequestContext(request))