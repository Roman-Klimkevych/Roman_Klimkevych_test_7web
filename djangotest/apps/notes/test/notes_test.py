from django_webtest import WebTest
from webtest import TestApp
from django.core.wsgi import get_wsgi_application
from django.core.urlresolvers import reverse
# from djangotest import settings
from django.conf import settings

class MyTestCase(WebTest):

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
        assert "Lorem ipsum dolor sit amet" in resp

    def test_notes_form(self):
        
        """ 
        Test the ability to add new text note. 

        Updated to work with Ajax.

        """

        """ Check that form.is_valid works as expected. """
        resp = self.app.get(reverse('text_notes'))
        form = resp.form
        res = self.app.post(reverse('ajax_notes'), 
                            {   
                                'csrfmiddlewaretoken':form['csrfmiddlewaretoken'].value,
                                'note': 'Note with more than 10 symbols'
                            },
                            headers = dict(X_REQUESTED_WITH='XMLHttpRequest'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.content_type, "application/javascript")
        assert "Your text note has been successfully added!!!" in res
        
        """ Check that form.is_invalid works as expected. """
        res = self.app.post(reverse('ajax_notes'), 
                            {   
                                'csrfmiddlewaretoken':form['csrfmiddlewaretoken'].value,
                                'note': '123456789'
                            },
                            headers = dict(X_REQUESTED_WITH='XMLHttpRequest'))
        self.assertEqual(res.status_code, 200)
        assert "Your note should contain at least 10 symbols!" in res

    def test_form_field(self):
        """ Test custom form field that returns notes changed to upper case."""
        resp = self.app.get(reverse('text_notes'))
        form = resp.form
        res = self.app.post(reverse('ajax_notes'), 
                            {   
                                'csrfmiddlewaretoken':form['csrfmiddlewaretoken'].value,
                                'note': 'Note changed to upper case'
                            },
                            headers = dict(X_REQUESTED_WITH='XMLHttpRequest'))
        self.assertEqual(res.status_code, 200)
        assert "NOTE CHANGED TO UPPER CASE" in res
        
    def test_total_count(self):
        """ Test total count of notes."""
        resp = self.app.get(reverse('text_notes'))
        form = resp.form
        res = self.app.post(reverse('ajax_notes'), 
                            {   
                                'csrfmiddlewaretoken':form['csrfmiddlewaretoken'].value,
                                'note': 'Text note number 2'
                            },
                            headers = dict(X_REQUESTED_WITH='XMLHttpRequest'))
        self.assertEqual(res.status_code, 200)
        assert '"count": 2' in res
        
    def test_image(self):
        
        """ Test ability to attach image to notes."""
        
        resp = self.app.get(reverse('text_notes'))
        form = resp.form
        root = settings.STATIC_ROOT
        img = root+'/img/image.jpg'
        
        res = self.app.post(
            url = reverse('ajax_notes'), 
            params = {
                'csrfmiddlewaretoken': form['csrfmiddlewaretoken'].value,
                'note': 'Text note number 2',
            } ,
            headers = dict(X_REQUESTED_WITH='XMLHttpRequest'),
            upload_files = [
                ('image', img)
            ]
        )
        self.assertEqual(res.status_code, 200)
        assert 'image.jpg' in res

        """ Check from submited without ajax"""
        form['note'] = "Note with more than 10 symbols"
        resp = form.submit(
            upload_files = [
                ('image', img)
            ])
        resp = resp.follow()
        self.assertEqual(resp.status_code, 200)
        assert 'image.jpg' in resp
        


