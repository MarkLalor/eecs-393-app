from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
import courseitem as ci
import uuid

class Document(db.Model):
    documentID = db.IntegerProperty()
    creator = db.StringProperty() # Case ID of the creator of the assignment.
    creationTime = db.DateTimeProperty()

    name = db.StringProperty() # Human-readable document name.

    #TODO: actual document hookup

class UserDocument(ndb.Model):
	user = ndb.StringProperty()
	blob_key = ndb.BlobKeyProperty()

class DocumentUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			upload = self.get_uploads()[0]
			print "printing out user info"
			username = users.get_current_user().nickname().split("@")[0]
			user_document = UserDocument(
				user=username,
				blob_key=upload.key())
			print "done adding to model"
			user_document.put()

			
			my_query = blobstore.BlobInfo.all()
			for blob_info in my_query:
				print str(blob_info.key())
			self.redirect('/upload_view_document/%s' % upload.key())

		except:
			self.error(500)

class ViewDocumentHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, document_key):
		if not blobstore.get(document_key):
			self.error(404)
		else:
			self.send_blob(document_key)

app = webapp2.WSGIApplication([
    ('/upload_document', DocumentUploadHandler),
    ('/upload_view_document/([^/]+)?', ViewDocumentHandler)
], debug=True)