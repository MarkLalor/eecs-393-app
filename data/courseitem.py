from google.appengine.ext import db
import course
import webapp2
import datetime
from random import randint
from google.appengine.api import users
from google.appengine.ext import blobstore
import json 

class CourseItem(db.Model):
    courseItemID = db.IntegerProperty()
    #courseID = db.StringProperty()
    courseID = db.IntegerProperty() # Course ID representing the course that this CourseItem is associated with.


    creator = db.StringProperty() # Case ID of the creator of the assignment.
    creationTime = db.DateTimeProperty()

    name = db.StringProperty() # Human-readable course item name.

    # Optional properties
    body = db.StringProperty() # Optional text describing the course item.
    assigned_date = db.DateTimeProperty()
    due_date = db.DateTimeProperty()

    documents = db.ListProperty(item_type=str,default=[]) # list of document IDs [see documentID of class Document(db.Model)]

    def getJSONRepresentation(self):
        #0: [{ courseItemId: 0, creator: "BOB", creationTime: "10/0/2017", name: "Assignment", body: "shared memory assignment", assigned_date: "10/2/2017", due_date: "10/25/2017"},
        integernum = int(self.courseItemID)
        print "printing out all items"
        print list(self.documents)

        json_rep = {"courseItemId":int(self.courseItemID),
                #"courseID": int(self.courseID),
                "creator": str(self.creator),
                "creationTime": str(self.creationTime.isoformat()),
                "name":str(self.name),
                "body":str(self.body),
                "assigned_date":str(self.assigned_date.isoformat()),
                "due_date":str(self.due_date.isoformat()),
                "documents":list(self.documents)}
        return json_rep

class CourseItemUpload(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()
        courseItemid = randint(0,1000)
        print courseItemid
        courseid = self.request.get("courseid")
        print courseid
        assignmentname = self.request.get("assignmentname")
        print assignmentname
        description = self.request.get("description")
        print description
        assigned_date = self.request.get("assigneddate")
        print assigned_date
        due_date = self.request.get("duedate")
        print due_date
        username = users.get_current_user().nickname().split("@")[0]
        print username

        adatetime_object = datetime.datetime.strptime(assigned_date, '%m/%d/%Y')
        ddatetime_object = datetime.datetime.strptime(due_date, '%m/%d/%Y')

        courseitem = CourseItem(
            courseItemID= courseItemid,
            courseID=int(courseid),
            creator= username,
            creationTime= datetime.datetime.now(),
            name = assignmentname,
            body= description,
            assigned_date= adatetime_object,
            due_date= ddatetime_object
            )

        courseitem.put()
        self.redirect('/')

app = webapp2.WSGIApplication([
    ('/add_assignment', CourseItemUpload)], debug=True)