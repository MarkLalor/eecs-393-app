from google.appengine.ext import db

class ChatMessage(db.Model):
    courseOrCourseItem = db.BooleanProperty()
    itemID = db.IntegerProperty() # Course ID or Course Item ID representing the object this chat message is associated with.

    creator = db.StringProperty() # Case ID of the creator of the assignment.
    creationTime = db.DateTimeProperty()

    body = db.StringProperty() # Optional text describing the course item.