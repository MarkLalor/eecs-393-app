import webapp2
from data.student import Student
from data.course import Course
from data.courseitem import CourseItem
from datetime import datetime


class Debug(webapp2.RequestHandler):
	@staticmethod
	def filldb():
		test_student = Student()
		test_student.caseID = "tkjdf328"
		test_student.name = "Testy Userman"
		test_student.courses = [1, 2, 3]
		test_student_key = test_student.put()

		test_course1 = Course()
		test_course1.courseID = 1
		test_course1.name = "Software Engineering"

		test_course1.department = "EECS"
		test_course1.number = 393
		test_course1.section = 100

		test_course1.year = 2016
		test_course1.term = 3

		test_course2 = Course()
		test_course2.courseID = 2
		test_course2.name = "Kinesiology for Dance"

		test_course2.department = "DANC"
		test_course2.number = 445
		test_course2.section = 100

		test_course2.year = 2017
		test_course2.term = 1

		test_course1_key = test_course1.put()
		test_course2_key = test_course2.put()

		test_courseitem = CourseItem()

		test_courseitem.courseItemID = 1
		test_courseitem.courseID = 1

		test_courseitem.creator = "tkjdf328"
		test_courseitem.creationTime = datetime.now()

		test_courseitem.name = "Software Design Document"

		test_courseitem.body = "This is the software design document description."
		test_courseitem.assigned_date = datetime.now()
		test_courseitem.due_date = datetime.now()

		test_courseitem_key = test_courseitem.put()

	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		
		if self.request.get('filldb') == 'true':
			Debug.filldb()
			self.response.out.write("Filled DB.")


app = webapp2.WSGIApplication([
	('/debug', Debug),
], debug=True)
