import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Some other data')


app = webapp2.WSGIApplication([
    ('/other', MainPage),
], debug=True)
