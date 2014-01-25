from django.contrib import messages
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin
from notes.models import Notes
from notes.forms import AddNoteForm

class NotesDisplay(FormMixin, ListView):
    queryset = Notes.objects.order_by('-id')    
    context_object_name = 'notes'
	
    def get_context_data(self, **kwargs):
        context = super(NotesDisplay, self).get_context_data(**kwargs)
        context['form'] = AddNoteForm()
        return context
	
class NotesFormProcessor(MultipleObjectMixin, FormView):
    queryset = Notes.objects.order_by('-id')
    form_class = AddNoteForm
    context_object_name = 'notes'
    template_name = 'notes/notes_list.html'

    def post(self, request, *args, **kwargs):
        form = AddNoteForm(request.POST)
        self.object_list = self.get_queryset()
        if form.is_valid():
            messages.success(request, "Your text note has been successfully added!!!")
            return self.form_valid(form)
        else:
            return super(NotesFormProcessor, self).form_invalid(form)
	
    def form_valid(self, form):
        note_id = Notes.objects.latest('id').id + 1
        new_note = form.cleaned_data['note']
        added_note = Notes(title="Note_" + str(note_id), text=new_note)
        added_note.save()
        return super(NotesFormProcessor, self).form_valid(form)
	
    def get_success_url(self):
        return reverse('text_notes')

class NotesView(View):

    def get(self, request, *args, **kwargs):
        view = NotesDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = NotesFormProcessor.as_view()
        return view(request, *args, **kwargs)