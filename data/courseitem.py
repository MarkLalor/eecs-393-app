from google.appengine.ext import db
import course
import webapp2
import datetime
from random import randint
from google.appengine.api import users


class CourseItem(db.Model):
    courseItemID = db.IntegerProperty()
    courseID = db.ReferenceProperty(course.Course) # Course ID representing the course that this CourseItem is associated with.

    creator = db.StringProperty() # Case ID of the creator of the assignment.
    creationTime = db.DateTimeProperty()

    name = db.StringProperty() # Human-readable course item name.

    # Optional properties
    body = db.StringProperty() # Optional text describing the course item.
    assigned_date = db.DateTimeProperty()
    due_date = db.DateTimeProperty()

    documents = db.ListProperty(item_type=int,default=[]) # list of document IDs [see documentID of class Document(db.Model)]

class CourseItemUpload(webapp2.RequestHandler):
    def post(self):
        courseItemid = randint(0,1000)
        courseid = self.request.get("courseid")
        assignmentname = self.request.get("assignmentname")
        description = self.request.get("description")
        assigned_date = self.request.get("assigneddate")
        due_date = self.request.get("duedate")
        username = users.get_current_user().nickname().split("@")[0]

        adatetime_object = datetime.strptime(assigned_date, '%m/%d/%Y')
        ddatetime_object = datetime.strptime(due_date, '%m/%d/%Y')

        courseitem = CourseItem(
            courseItemID= courseItemid,
            courseID=courseid,
            creator= username,
            creationTime= datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"),
            name = assignmentname,
            body= description,
            assigned_date= adatetime_object,
            due_date= ddatetime_object,
            documents=None
            )

        courseitem.put()

app = webapp2.WSGIApplication([
    ('/add_assignment', CourseItemUpload)], debug=True)