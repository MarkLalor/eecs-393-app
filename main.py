import webapp2
import json
import os

from google.appengine.api import users
import urllib2
from canvas_sdk import RequestContext
from canvas_sdk.methods import sections
from canvas_sdk.methods import courses

import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
''' python dev_appserver.py C://Vimig/SoftwareEng/mainApp/eecs-393-app/app.yaml '''

class MainPage(webapp2.RequestHandler):
	# @staticmethod
	# def html_print(request, filename, *parts):
	# 	with open('web/html/' + filename + '.html', 'r') as content_file:
	# 		print content_file.read() % parts
	# 		request.response.out.write(content_file.read() % parts)
	# 		request.response.out.write("\n")

	def get(self):

		user = users.get_current_user()
		#log in requirement as a handler in the yaml file
		#additional failsafe here, can be removed
		if not user:
			login_url = users.create_login_url('/')
			self.redirect(login_url)

		oauth_token = "5590~AiNzEe2sqfpgQuKEn6vCoHUG1x8PTt0VniscrvG8gSp0hke4OW5jciN0maBxm9QQ"
		base_api_url = 'https://canvas.case.edu/api'
		
		rc = RequestContext(oauth_token, base_api_url)
		results = courses.list_your_courses(rc, "needs_grading_count")
		courseJSON = results.content


		nickname = user.nickname() #for debugging
		logout_url = users.create_logout_url('/');

		self.response.headers['Content-Type'] = 'text/html'

		#TODO: memcache the different files here
		config = {}
		with open('config.json', 'r') as config_file:
			config = json.load(config_file)

		template_values = {
			'config_header': config['header'],
			'nickname': nickname,
			'logout_url': logout_url,
		}

		template = JINJA_ENVIRONMENT.get_template('web/html/body.html')
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
