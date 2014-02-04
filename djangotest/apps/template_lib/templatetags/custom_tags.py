from django import template
from notes.models import Notes

register = template.Library()

@register.inclusion_tag('text_note.html')
def text_note(note_id):
	note = Notes.objects.get(id=note_id)
	text = note.text
	return {"text": text}