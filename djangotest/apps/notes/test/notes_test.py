from django_webtest import WebTest
from webtest import TestApp
from django.core.wsgi import get_wsgi_application
from django.core.urlresolvers import reverse

class MyTestCase(WebTest):

    """
    Create test case for testing notes application

    First test case gets some initial data and application to be tested, 
    then each function tests single task to be completed

    """

    """ Some initial data """
    fixtures = ['initial_data.json']
    
    """ Application to be tested """
    application = get_wsgi_application()
    app = TestApp(application)
    

    def test_notes(self):
        
        """ Test that app shows list of text notes """

        """ Check response status """
        resp = self.app.get(reverse('text_notes'))
        self.assertEqual(resp.status_code, 200)
        
        """ Check text note in response """
        assert "Lorem ipsum dolor sit amet" in resp

    def test_notes_form(self):
        
        """ Test the abilit to add new text note """

        """ Check that form.is_valid works as expected """
        resp = self.app.get(reverse('text_notes'))
        form = resp.form
        form['note'] = "Note with more than 10 symbols"
        res = form.submit()
        self.assertEqual(res.status_code, 302)
        resp = self.app.get(reverse('text_notes'))
        assert "Your text note has been successfully added!!!" in resp

        """ Check that form.is_invalid works as expected """
        form['note'] = '123456789'
        res = form.submit()
        self.assertEqual(resp.status_code, 200)
        assert "Your note should contain at least 10 symbols!" in res

    def test_form_field(self):
        """ Test custom form field that returns notes changed to upper case"""
        resp = self.app.get(reverse('text_notes'))
        form = resp.form
        form['note'] = "Note changed to upper case"
        res = form.submit()
        self.assertEqual(res.status_code, 302)
        resp = self.app.get(reverse('text_notes'))
        assert "NOTE CHANGED TO UPPER CASE" in resp