from google.appengine.ext import db
import course
import webapp2
from google.appengine.ext import blobstore 
import datetime
from random import randint
from google.appengine.api import users
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

    documents = db.ListProperty(str,default=[]) # list of document IDs [see documentID of class Document(db.Model)]

    def getJSONRepresentation(self):
        #0: [{ courseItemId: 0, creator: "BOB", creationTime: "10/0/2017", name: "Assignment", body: "shared memory assignment", assigned_date: "10/2/2017", due_date: "10/25/2017"},
        integernum = int(self.courseItemID)
        json_rep = {"courseItemId":int(self.courseItemID),
                #"courseID": int(self.courseID),
                "Creator": str(self.creator),
                "Time Created": str(str(self.creationTime.month) + "/" + 
                    str(self.creationTime.day) + "/" + str(self.creationTime.year) + " " +
                    str(self.creationTime.hour)+":"+str(self.creationTime.minute)),
                "Name":str(self.name),
                "Description":str(self.body),
                "Assigned Date":str(str(self.assigned_date.month) + "/" + 
                    str(self.assigned_date.day) + "/" + str(self.assigned_date.year) + " " +
                    str(self.assigned_date.hour)+":"+str(self.assigned_date.minute)),
                "Due Date":str(str(self.due_date.month) + "/" + 
                    str(self.due_date.day) + "/" + str(self.due_date.year) + " " +
                    str(self.due_date.hour)+":"+str(self.due_date.minute)),
                "documents":list(self.documents)}

        return json.dumps(json_rep)

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

        adatetime_object = datetime.datetime.strptime(assigned_date, '%Y-%m-%d')
        ddatetime_object = datetime.datetime.strptime(due_date, '%Y-%m-%d')

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