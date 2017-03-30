import webapp2
import json
from google.appengine.ext import blobstore
from google.appengine.api import users

class MainPage(webapp2.RequestHandler):
	@staticmethod
	def html_print(request, filename, *parts):
		with open('web/html/' + filename + '.html', 'r') as content_file:
			request.response.out.write(content_file.read() % parts)
			request.response.out.write("\n")

	def get(self):

		user = users.get_current_user()
		#log in requirement as a handler in the yaml file
		#additional failsafe here, can be removed
		upload_url = blobstore.create_upload_url('/upload_document')
		if not user:
			login_url = users.create_login_url('/')
			self.redirect(login_url)

		nickname = user.nickname() #for debugging
		logout_url = users.create_logout_url('/');

		self.response.headers['Content-Type'] = 'text/html'

		#TODO: memcache the different files here
		config = {}
		with open('config.json', 'r') as config_file:
			config = json.load(config_file)

		MainPage.html_print(self, 'page_header')
		MainPage.html_print(self, 'body_header', config['header'],nickname,logout_url)
		MainPage.html_print(self, 'body', upload_url)
		MainPage.html_print(self, 'body_footer')
		MainPage.html_print(self, 'page_footer')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
