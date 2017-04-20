import webapp2
import json
from google.appengine.ext import blobstore
import os
import datetime

from google.appengine.api import users
from google.appengine.ext import db

import urllib2
from canvas_sdk import RequestContext
from canvas_sdk.methods import sections
from canvas_sdk.methods import courses
from canvas_sdk.methods import users as canvas_users
from data.student import Student
from data.course import Course
from data.courseitem import CourseItem
from random import randint

import jinja2

OAUTH_TOKEN_LIST = {
	"vxs215" : "5590~AiNzEe2sqfpgQuKEn6vCoHUG1x8PTt0VniscrvG8gSp0hke4OW5jciN0maBxm9QQ", #vimig
	"sam274":"5590~vWLHNZnYftuklmDGxti7Mo7Xvi25o3HpjlDRiRwlK9KBzVj2UxhNEsZoDX6RZYxD", #stephen
	"eaf53": "5590~ObS2t1n5sI3ROknzhtgYY3pZ29DdbINz4JBV6E8eQC0AjRgAldCbb7meylvfrRWK", #ethan
	"yfm": "5590~yZZea5tLKykn5iPbu8HykFEMQLl2WM3RUR185VYculffDXV7JsOlS1jJJ8Ed0dZk", #yousef
	"mmh124": "5590~IXIFbF2Bs4DPMjRisp0EKaz5k6dM6pNQzyoSnHIMz12m2spWpBGBlahhZqtLrg99", #Haus
	"dxb448" : "5590~eRWgUDGbDMy6SXJObBiici05IAu12K8h1cTartJHPFzCTVe2KLdaxvktbf1BOru5", #dina
}
''' python dev_appserver.py C://Vimig/SoftwareEng/mainApp/eecs-393-app/app.yaml '''
class MainPage(webapp2.RequestHandler):
	def get(self):

		user = users.get_current_user()
		caseID = user.nickname().split("@")[0]
		nickname = user.nickname()

		if caseID in OAUTH_TOKEN_LIST.keys():
			oauth_token = OAUTH_TOKEN_LIST[caseID]	
		else:
			oauth_token = OAUTH_TOKEN_LIST['vxs215']

		base_api_url = 'https://canvas.case.edu/api'

		cas_url = ""

		rc = RequestContext(oauth_token, base_api_url, timeout=60)
		rc2 = RequestContext(oauth_token, base_api_url, timeout=60)
		#db.GqlQuery("SELECT * FROM Course WHERE courseID = :1", courseID).get()
		
		print(user)
		#log in requirement as a handler in the yaml file
		#additional failsafe here, can be removed
		upload_url = blobstore.create_upload_url('/upload_document')
		print("printing upload_url")
		print(upload_url)
		if not user:
			login_url = users.create_login_url('/')
			self.redirect(login_url)


		
		q1 = Student.gql("WHERE caseID = :1", caseID)
		returningUser = q1.get()

		#to be used for the template render view for course info
		courses_render = []

		firstTimeUser = None
		if not returningUser:
			userInfo =  canvas_users.get_my_user_profile(rc)
			userInfoJSON = json.loads(userInfo.content)
			results = courses.list_your_courses(rc2, include=["term", "sections"])
			courseJSON = json.loads(results.content) 
			course_id_list = []
			course_obj_list = []
			for course in courseJSON:
				course_id_list.append(course['id'])
				#course_term = [spring, 2017]
				course_term = course['term']['name'].split(' ')
				#course_code = [department, SIS course number]
				course_code = course['course_code'].split(' ')

				if not self.RepresentsInt(course_code[1]):
					course_code[0] = None
					course_code[1] = None
				else:
					course_code[1] = int(course_code[1])

				if len(course_term) < 2:
					course_term[0] = None
					course_term.append(None)
				elif not self.RepresentsInt(course_term[1]):
					course_term[0] = None
					course_term[1] = None
				else:
					course_term[1] = int(course_term[1])
				
				course_name = course['name'].split("(")
				course_section = None
				if len(course_name) > 1:
					course_section = int(course_name[1].split('/')[0])

				db_course = Course(courseID=int(course['id']), 
					name=course_name[0],
					department=course_code[0],
					number = course_code[1],
					section = course_section,
					year = course_term[1],
					term =course_term[0])
				
				course_obj_list.append(db_course)

			courses_render = course_obj_list

			for course in course_obj_list:
				course.put()
			firstTimeUser = Student(caseID=caseID, name=userInfoJSON['name'],courses=course_id_list)
			firstTimeUser.put()

		curr_user = None
		if firstTimeUser:
			curr_user = firstTimeUser
		elif returningUser:
			curr_user = returningUser
		else:
			self.error(500)

		curr_user_courseID_list = curr_user.courses

		#check if there is annything in the courses (would only happen if the user is just being created)
		if not courses_render:
			for courseID in curr_user_courseID_list:
				q1 = Course.gql("WHERE courseID = :1", courseID)
				courses_render.append(q1.get())
		
		course_item_list = {}
		#{courseID: [CourseItem1, CourseItem2] }
		for courseID in curr_user_courseID_list:
			q2 = CourseItem.gql("WHERE courseID = :1", courseID)
			course_item_list[int(courseID)] = []
			for course_item in q2:
				print course_item
				course_item_list[int(courseID)].append(course_item.getJSONRepresentation())

		nickname = user.nickname() #for debugging
		logout_url = users.create_logout_url('/');

		self.response.headers['Content-Type'] = 'text/html'

		#TODO: memcache the different files here
		config = {}
		with open('config.json', 'r') as config_file:
			config = json.load(config_file)

		template_values = {
			'config_header': config['header'],
			'nickname': nickname,
			'logout_url': logout_url,
			'courses': courses_render,
			'course_items': course_item_list,
			'upload_url': upload_url,
		}

		template = MainPage.JINJA_ENVIRONMENT.get_template('web/html/body.html')
		self.response.write(template.render(template_values))

	JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True,
    auto_reload=True)

	# @staticmethod
	# def html_print(request, filename, *parts):
	# 	with open('web/html/' + filename + '.html', 'r') as content_file:
	# 		print content_file.read() % parts
	# 		request.response.out.write(content_file.read() % parts)
	# 		request.response.out.write("\n")
	print 'reached GET!!!!!!!!!!!!!!'

	def RepresentsInt(self, s):
	    try:
	    	int(s)
	    	return True
	    except ValueError:
	    	return False

app = webapp2.WSGIApplication([('/', MainPage),], debug=True)

