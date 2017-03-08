from google.appengine.ext import db

class CourseItem(db.Model):
    courseItemID = db.IntegerProperty()
    courseID = db.IntegerProperty() # Course ID representing the course that this CourseItem is associated with.

    creator = db.StringProperty() # Case ID of the creator of the assignment.
    creationTime = db.DateTimeProperty()

    name = db.StringProperty() # Human-readable course item name.

    # Optional properties
    body = db.StringProperty() # Optional text describing the course item.
    assigned_date = db.DateTimeProperty()
    due_date = db.DateTimeProperty()

    documents = db.ListProperty(item_type=int,default=[]) # list of document IDs [see documentID of class Document(db.Model)]