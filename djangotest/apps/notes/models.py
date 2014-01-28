from django.db import models
from notes.forms import UpperCaseField

class UpperCaseTextField(models.TextField):

    """
    Create custom text field that returns notes changed to uppercase in the admin interface.
    """

    def formfield(self, **kwargs):    
        return models.Field.formfield(self, UpperCaseField, **kwargs)

class Notes(models.Model):

    """
    Create model for text notes that contains note title and note text.
    """

    title = models.CharField(max_length=100, blank=True, verbose_name='note title')
    text = UpperCaseTextField(verbose_name='note text',)
        
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'