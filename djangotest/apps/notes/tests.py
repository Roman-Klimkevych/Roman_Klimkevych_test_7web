from django.test import TestCase

class NotesViewsTestCase(TestCase):
	fixtures = ['notes_views_testdata.json']

	def test_index(self):
		resp = self.client.get('/')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('notes' in resp.context)
		self.assertEqual([notes.pk for notes in resp.context['notes']], [1])
		note_1 = resp.context['notes'][0]
		self.assertEqual(note_1.text, 'Lorem ipsum dolor sit amet')
		resp = self.client.get('/notes/')
		self.assertEqual(resp.status_code, 404)