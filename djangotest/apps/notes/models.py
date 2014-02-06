from django.db import models
from notes.forms import UpperCaseField
from django.dispatch import receiver

class UpperCaseTextField(models.TextField):

    """
    Create custom text field that returns notes changed to uppercase in the admin interface.
    """

    def formfield(self, **kwargs):    
        return models.Field.formfield(self, UpperCaseField, **kwargs)

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^notes\.models\.UpperCaseTextField"])


class Notes(models.Model):

    """
    Create model for text notes that contains note title and note text.
    """

    title = models.CharField(max_length=100, blank=True, verbose_name='note title')
    text = UpperCaseTextField(verbose_name='note text',)
    image = models.ImageField(upload_to="uploads", blank=True, verbose_name='attached image')
    books = models.ManyToManyField('Book', related_name="notes",)
        
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

class Book(models.Model):

    """
    Create model for Books to store notes.
    """
    title = models.CharField(max_length=100, blank=True, verbose_name='Book title')
    
    def __unicode__(self):
        return self.title

    


@receiver(models.signals.pre_delete, sender=Notes)
def handle_deleted_notes(sender, instance, **kwargs):
    """ 
    Delete book when last not is deleted.

    Check the books that contained the text note which is going to be deleted.
    If this book contains one last note, delete this book.

     """
    books_touched = Book.objects.filter(notes=instance)
    for book in books_touched:
        book_len = sender.objects.filter(books=book).count()
        if book_len == 1:
            book.delete()
