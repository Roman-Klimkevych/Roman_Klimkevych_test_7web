from django_webtest import WebTest
from webtest import TestApp
from django.core.wsgi import get_wsgi_application

class MyTestCase(WebTest):

    # some initial data
    fixtures = ['notes_views_testdata.json']
    
    # application to be tessted
    application = get_wsgi_application()
    app = TestApp(application)
    

    def testNotes(self):
        # check response status
        resp = self.app.get('/')
        assert resp.status == '200 OK'
        
        # check text note in response
        assert 'Lorem ipsum dolor sit amet' in resp