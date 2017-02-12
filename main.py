import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('eecs-393-app! using webapp2')


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
