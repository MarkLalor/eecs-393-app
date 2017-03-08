import webapp2
import json

class MainPage(webapp2.RequestHandler):
	@staticmethod
	def html_print(request, filename, *parts):
		with open('web/html/' + filename + '.html', 'r') as content_file:
			request.response.out.write(content_file.read() % parts)
			request.response.out.write("\n")

	def get(self):
		self.response.headers['Content-Type'] = 'text/html'

		config = {}
		with open('config.json', 'r') as config_file:
			config = json.load(config_file)

		MainPage.html_print(self, 'page_header')
		MainPage.html_print(self, 'body_header', config['header'])
		MainPage.html_print(self, 'body')
		MainPage.html_print(self, 'body_footer')
		MainPage.html_print(self, 'page_footer')

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
