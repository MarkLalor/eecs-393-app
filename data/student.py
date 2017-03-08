from google.appengine.ext import db

class Student(db.Model):
    caseID = db.StringProperty()
    name = db.StringProperty()
    lastLogin = db.DateTimeProperty()

    courses = db.ListProperty(item_type=int,default=[]) # list of course IDs [see courseID of class Course(db.Model)]