from google.appengine.ext import db

class Document(db.Model):
    documentID = db.IntegerProperty()
    creator = db.StringProperty() # Case ID of the creator of the assignment.
    creationTime = db.DateTimeProperty()

    name = db.StringProperty() # Human-readable document name.

    #TODO: actual document hookup