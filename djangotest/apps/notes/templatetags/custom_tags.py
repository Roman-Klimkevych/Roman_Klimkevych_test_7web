from django import template
from notes.models import Notes

register = template.Library()

@register.inclusion_tag('text_note.html')
def text_note(note_id):
	""" 
    Create custom inclusion template tag 
    that will render one text note by given id
    """
	note = Notes.objects.get(id=note_id)
	text = note.text
	return {"text": text}