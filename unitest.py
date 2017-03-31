import webtest 
import unittest
import main
import webapp2
from google.appengine.ext import testbed

from google.appengine.api import users


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_user_stub()

    def tearDown(self):
        self.testbed.deactivate()

    def loginUser(self, email='user@example.com', id='123', is_admin=False):
        self.testbed.setup_env(
            user_email=email,
            user_id=id,
            user_is_admin='1' if is_admin else '0',
            overwrite=True)

    def testLogin(self):
        self.assertFalse(users.get_current_user())
        self.loginUser()
        self.assertEquals(users.get_current_user().email(), 'user@example.com')
        self.loginUser(is_admin=True)
        self.assertTrue(users.is_current_user_admin())
        self.loginUser('', '')
        self.assertFalse(users.get_current_user())
        self.loginUser('test@example.com', '123')
        self.assertFalse(users.is_current_user_admin())
        self.loginUser('test@example.com', '123', is_admin=True)
        self.assertTrue(users.is_current_user_admin())
        self.assertEquals(users.get_current_user().email(), 'test@example.com')
        self.assertEquals(users.get_current_user().user_id(), '123')
'''
class AppTest(unittest.TestCase):
    def setUp(self):
        app = webapp2.WSGIApplication([('/', main.MainPage)])
        self.testapp = webtest.TestApp(app)
        self.testbed = testbed.Testbed()
        self.testbed.activate()

    def tearDown(self):
    	self.testbed.deactivate()

    # Test the handler.
    def testHelloWorldHandler(self):
        response = self.testapp.get('/')
        self.testbed.init_blobstore_stub
        self.assertEqual(response.status_int, 200)
        #self.assertEqual(response.normal_body, 'Hello World!')
        self.assertEqual(response.content_type, 'text/plain')

'''
'''
class HelloWorldTest(unittest.TestCase):
    def test_index(self):
    	app = TestApp(main.app)
        """Tests that the index page for the application

        The page should be served as: Content-Type: text/plain
        The body content should contain the string: Hello world!
        """
        response = app.get('/')
        self.assertEqual(response.content_type, 'text/html')
        #self.assertIn('Hello world!', response.body)
        '''