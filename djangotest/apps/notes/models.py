from django.db import models

class Notes(models.Model):

    """
    Create model for text notes that contains note title and note text.
    """

    title = models.CharField(max_length=100, blank=True, verbose_name='note title')
    text = models.TextField(verbose_name='note text',)
        
    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'