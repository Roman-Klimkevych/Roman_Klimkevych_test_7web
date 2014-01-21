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