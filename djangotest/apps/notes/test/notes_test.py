from django_webtest import WebTest
from webtest import TestApp
from django.core.wsgi import get_wsgi_application
from django.core.urlresolvers import reverse

class MyTestCase(WebTest):

    # some initial data
    fixtures = ['initial_data.json']
    
    # application to be tessted
    application = get_wsgi_application()
    app = TestApp(application)
    

    def testNotes(self):
        # check response status
        resp = self.app.get(reverse('text_notes'))
        assert resp.status == '200 OK'
        
        # check text note in response
        assert 'Lorem ipsum dolor sit amet' in resp

    def testNotesForm(self):
        # check form.is_valid
        resp = self.app.get(reverse('text_notes'))
        form = resp.form
        form['note'] = 'Note with more than 10 symbols'
        res = form.submit()
        assert res.status_int == 302
        resp = self.app.get(reverse('text_notes'))
        assert 'Your text note has been successfully added!!!' in resp

        # check form.is_invalid
        form['note'] = '123456789'
        res = form.submit()
        assert res.status_int == 200
        assert 'Your note should contain at least 10 symbols!' in res
