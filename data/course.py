from google.appengine.ext import db

class Course(db.Model):
    courseID = db.IntegerProperty() # Unique ID used only by the application for mapping.

    name = db.StringProperty() #Human-readable course name.

    department = db.StringProperty()   # e.g. EECS
    courseNumber = db.StringProperty() # e.g. 393

    year = db.IntegerProperty() # e.g. 2017
    term = db.IntegerProperty() # 0, 1, 2 for fall, spring, summer. Some sort of enumeration solution would be more ideal.