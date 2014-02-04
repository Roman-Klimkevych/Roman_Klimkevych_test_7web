from django_webtest import WebTest
from webtest import TestApp
from django.core.wsgi import get_wsgi_application
from django.conf.urls import patterns, include, url



class MyTestCase(WebTest):

    # optional: we want some initial data to be able to login
    fixtures = ['notes_views_testdata.json']
    application = get_wsgi_application()
    app = TestApp(application)
    # optional: default extra_environ for this TestCase
    #extra_environ = {'HTTP_ACCEPT_LANGUAGE': 'ru'}

    def testNotes(self):

        resp = self.app.get('/')
        assert resp.status == '200 OK'
        # resp.mustcontain('<html>')
        assert 'Lorem ipsum dolor sit amet' in resp
        
        # pretend to be logged in as user `kmike` and go to the index page
        #index = self.app.get('/', user='kmike')
        #resp = self.client.get('/')
        #self.assertEqual(resp.status_code, 200)
        # All the webtest API is available. For example, we click
        # on a <a href='/tech-blog/'>Blog</a> link, check that it
        # works (result page doesn't raise exceptions and returns 200 http
        # code) and test if result page have 'My Article' text in
        # it's body.
        #assert 'My Article' in index.click('Blog')