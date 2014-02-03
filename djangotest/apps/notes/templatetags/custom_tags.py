from django import template
from notes.models import Notes
import re

register = template.Library()

@register.inclusion_tag('text_note.html')
def text_note(note_id):
    """ 
    Create custom inclusion template tag 
    that will render one text note by given id
    """
    note = Notes.objects.get(id=note_id)
    text = note.text
    image = note.image
    return {'text': text, 'image': image}

@register.filter(is_safe=True)
def stripwhitespace(value):
    inbetween = re.compile('>[ \r\n]+<')
    newlines = re.compile('\r|\n')
    return newlines.sub('', inbetween.sub('><', value))
