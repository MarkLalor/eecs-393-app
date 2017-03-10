from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2

class Document(db.Model):
    documentID = db.IntegerProperty()
    creator = db.StringProperty() # Case ID of the creator of the assignment.
    creationTime = db.DateTimeProperty()

    name = db.StringProperty() # Human-readable document name.

    #TODO: actual document hookup

class UserDocument(ndb.Model):
	user = ndb.StringProperty()
	print user
	blob_key = ndb.BlobKeyProperty()

class DocumentUploadFormHandler(webapp2.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/upload_document')
		self.response.out.write("""
			<html><body>
<form action="{0}" method="POST" enctype="multipart/form-data">
  Upload File: <input type="file" name="file"><br>
  <input type="submit" name="submit" value="Submit">
</form>
</body></html>""".format(upload_url))


class DocumentUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			upload = self.get_uploads()[0]
			print "printing out user info"
			print user.get_current_user().user_id()
			user_document = UserDocument(
				user=user.get_current_user().user_id(),
				blob_key=upload.key())
			user_document.put()

			self.redirect('/view_document/%s' % upload.key())

		except:
			self.error(500)

class ViewDocumentHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, document_key):
		if not blobstore.get(document_key):
			self.error(404)
		else:
			self.send_blob(document_key)

app = webapp2.WSGIApplication([
    ('/upload', DocumentUploadFormHandler),
    ('/upload_document', DocumentUploadHandler),
    ('/view_document/([^/]+)?', ViewDocumentHandler)
], debug=True)
