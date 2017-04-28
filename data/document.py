from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
from data.courseitem import CourseItem
import uuid
from HTMLParser import HTMLParser

class HelperDocument(ndb.Model):
	blob_key_string = ndb.StringProperty()
	blob_key = ndb.BlobKeyProperty()
    #TODO: actual document hookup

class UserDocument(ndb.Model):
	user = ndb.StringProperty()
	blob_key_string = ndb.StringProperty()
	blob_key = ndb.BlobKeyProperty()
	courseitemid = ndb.IntegerProperty()

	def getJSONRepresentation(self):
		json_rep = {"user": self.user, "blob_key": str(self.blob_key), "courseitemid": str(courseitemid)}

class DocumentUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			
			upload = self.get_uploads()[0]
			courseitemid = self.request.get("courseitemid")
			username = users.get_current_user().nickname().split("@")[0]
			uploadDocID = str(id(upload.key()))

			user_document = UserDocument(
				user=username,
				blob_key=upload.key(),
				blob_key_string=str(upload.key()),
				courseitemid=int(courseitemid))

			helper_document = HelperDocument(
				blob_key_string= str(upload.key()),
				blob_key=upload.key())
			
			helper_document.put()
			user_document.put()

			q = CourseItem.gql("WHERE courseItemID = :1", int(courseitemid))
			
			courseitem = q.get()
			courseitem.documents.append(upload.filename + ":" + str(upload.key()) + ":" + username)
			
			courseitem.put()	
			my_query = blobstore.BlobInfo.all()
			
			self.redirect('/')

		except:
			self.error(500)

class ViewDocumentHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, document_key):
		if not blobstore.get(document_key):
			self.error(404)
		else:
			self.send_blob(document_key)

class RemoveDocumentHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self,request):
		try:
			url = self.request.url
			key_cid = url.split("/upload_remove_document/")[1]
			key_cid_split = key_cid.split(":")
			parser = HTMLParser()
			q = CourseItem.gql("WHERE courseItemID = :1", int(key_cid_split[1]))
			courseitem = q.get()
			bk = ''
			for i in courseitem.documents:
				bk = i.split(":")
				if(key_cid_split[0].replace("%3D", "=") == bk[1]):
					courseitem.documents.remove(i)
			courseitem.put()
			blobkey = UserDocument.gql("WHERE blob_key_string= :1", bk[1]).get()
			blobstore.delete(bk[1])
			blobkey.key.delete()
			self.redirect('/')

		except:
			self.error(500)

app = webapp2.WSGIApplication([
    ('/upload_document', DocumentUploadHandler),
    ('/upload_view_document/([^/]+)?', ViewDocumentHandler),
    ('/upload_remove_document/([^/]+)?', RemoveDocumentHandler)
], debug=True)