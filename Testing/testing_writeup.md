Writeup regarding code coverage for demo 2
-------------------------------------------

We were able to test code coverage for all of our backend models, particularly, course, course_item, and student. In all of these, we achieved nearly 100% coverage through our tests. However, we were unable to test the "CourseItemUpload" request handler in the course_item test since we were testing backend data model interactions, and didn't perform any web testing from a code coverage perspective. Therefore, we only achieved 48% for the course item, since we still tested creating course items and saving them to the database. 

We were only able to test 22% of the main.py file, since the majority of that file was interactions to load the database and display it. The 22% came mainly from the import statements, so in order to test this more functionally, we need to create more tests that employ the application, as opposed to unit tests regarding the data model in general. This included interactions with a front-end python template engine and request handlers for the first page load.

Finally, we can see that some requests were tested through the python HTTP library urllib3, as can be seen from the requests_py.html test, achieving 83%. Additionally, from the webtest_py.html file, we can see that many of the libraries needed for web development could be loaded (100%), but we didn't test their functionality. 

Moving forward, we will be testing, from a code coverage perspective, the chat interactions with Firebase, and the front-end http requests to the datastore. 