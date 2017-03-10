import webapp2
import json
from google.appengine.api import users
from google.appengine.ext import db
from data.student import Student
from data.course import Course
from data.courseitem import CourseItem

class Request(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/json'
		caseID = users.get_current_user().nickname().split("@")[0]

		data_requested = self.request.get('data')

		# Important: Needs caching
		if data_requested == 'student':
			q = db.GqlQuery("SELECT * FROM Student WHERE caseID = :1", caseID)
			student = q.get()

			output = {}

			output['caseID'] = caseID
			output['name'] = student.name
			output['lastLogin'] = student.lastLogin
			
			output['courses'] = []
			for courseID in student.courses:
				course = db.GqlQuery("SELECT * FROM Course WHERE courseID = :1", courseID).get()

				if not course is None:
					course_output = {}
					course_output['id'] = courseID
					course_output['name'] = course.name
					course_output['department'] = course.department
					course_output['number'] = course.number
					course_output['section'] = course.section
					course_output['year'] = course.year
					course_output['term'] = course.term

					output['courses'].append(course_output)

			self.response.out.write(json.dumps(output))

		elif data_requested == 'course':
			courseID = self.request.get('courseID')
			# stub for later, most essential course data provided already in request?data=student

		elif data_requested == 'courseitems':
			courseID = self.request.get('courseID')

			query = db.GqlQuery("SELECT * FROM CourseItem WHERE courseID = :1", int(courseID))

			output = []

			for item in query.run(limit=20):
				course_item_output = {}

				course_item_output['courseItemID'] = item.courseItemID
				course_item_output['courseID'] = item.courseID
				course_item_output['creator'] = item.creator
				course_item_output['creationTime'] = item.creationTime.isoformat()
				course_item_output['name'] = item.name
				course_item_output['body'] = item.body
				course_item_output['assigned_date'] = item.assigned_date.isoformat()
				course_item_output['due_date'] = item.due_date.isoformat()
				course_item_output['documents'] = item.documents

  				output.append(course_item_output);


			self.response.out.write(json.dumps(output))



app = webapp2.WSGIApplication([
    ('/request', Request),
], debug=True)
