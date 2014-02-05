from django_webtest import WebTest
from webtest import TestApp
from notes.models import Notes
from django.core.urlresolvers import reverse
from django.core.wsgi import get_wsgi_application
from django.conf.urls import patterns, include, url
import re
from django.template import Template, Context, TemplateSyntaxError


class NotesTestCase(WebTest):

    """
    Create test case for testing notes application.

    First test case gets some initial data and application to be tested, 
    then each function tests single task to be completed.

    """

    """ Some initial data. """
    fixtures = ['initial_data.json']
    
    """ Application to be tested. """
    application = get_wsgi_application()
    app = TestApp(application)

    def test_notes(self):
        
        """ Test that app shows list of text notes. """

        """ Check response status. """
        resp = self.app.get(reverse('text_notes'))
        self.assertEqual(resp.status_code, 200)
        
        """ Check text note in response. """
        assert 'Lorem ipsum dolor sit amet' in resp
        

    def test_custom_tag(self):

        """ Test custom inclusion tag. """

        """ Check response status. """
        
        resp = self.app.get(reverse('text_notes'))
        self.assertEqual(resp.status_code, 200)
        
        """ Check custom template tag functionality in response. """
        
        note = Notes.objects.create(title='Note_1', text="Text Note")
        t = Template('{% load custom_tags %}{% text_note id %}')
        c = Context({"id": note.id})
        resp = t.render(c)
        assert '<p class="text-note">Text Note</p>' in resp
