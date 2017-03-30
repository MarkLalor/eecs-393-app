/** Appends Courses to the Course section Expecting JSON:
{
	courseID: [
		{course: STRING,
		 department: STRING, 
		 courseNumber: STRING, 
		 year : integer, 
		 term : integer}
	],
}
**/

function openCourseItems(courseID, course_item_list){
	console.log(courseID)

	course_items = course_item_list[courseID]
	console.log(course_items)
}
function populateCourses(courseJSON) {
	console.log(courseJSON)
	for (var i in courseJSON) {

		// Create tag
		var course = document.createElement('p');
		course.innerHTML = createCoursesString(courseJSON, i);
		course.id = i; // id is the courseID
		course.addEventListener("click", populateCourseItems);

		// Append to div
		var courseDiv = document.getElementById("courses");
		courseDiv.appendChild(course);
	}
}

/** 
DUMMY DATA
**/
var courseItemJSON= {
	0: [{ courseItemId: 0, creator: "BOB", creationTime: "10/0/2017", name: "Assignment", body: "shared memory assignment", assigned_date: "10/2/2017", due_date: "10/25/2017"},
		{ courseItemId: 1, creator: "BOB0", creationTime: "10/0/2017", name: "Assignment0", body: "shared memory assignment", assigned_date: "10/2/2017", due_date: "10/25/2017"},
		{ courseItemId: 2, creator: "BOB00", creationTime: "10/0/2017", name: "Assignment00", body: "shared memory assignment", assigned_date: "10/2/2017", due_date: "10/25/2017"},
		{ courseItemId: 3, creator: "BOB000", creationTime: "10/0/2017", name: "Assignment000", body: "shared memory assignment", assigned_date: "10/2/2017", due_date: "10/25/2017"},
		{ courseItemId: 4, creator: "BOB0000", creationTime: "10/0/2017", name: "Assignment0000", body: "shared memory assignment", assigned_date: "10/2/2017", due_date: "10/25/2017"}
		],
	1: [{ courseItemId: 1, creator: "BOB1", creationTime: "10/1/2017", name: "Assignment1", body: "Linked Lists", assigned_date: "10/2/2017", due_date: "10/25/2017"}],
	2: [{ courseItemId: 2, creator: "BOB2", creationTime: "10/2/2017", name: "Assignment2", body: "eigen values", assigned_date: "10/2/2017", due_date: "10/25/2017"}],
	3: [{ courseItemId: 3, creator: "BOB3", creationTime: "10/3/2017", name: "Assignment3", body: "sheet reading", assigned_date: "10/2/2017", due_date: "10/25/2017"}],
}

/** 
DUMMY DATA
**/

function populateCourseItems(tar) {
	var courseID = tar.target.id;
	var courseItems;
	var courseItemDiv = document.getElementById("courseItems");

	// basically the table look up: courseItems = getTable(courseID)
	for (var i in courseItemJSON) {
		if (i == courseID) {
			courseItems = courseItemJSON[i];
			break;
		}
	}
	
	// clear current list
	while (courseItemDiv.firstChild) {
   	 	courseItemDiv.removeChild(courseItemDiv.firstChild);
	}

	for (var i in courseItems) {
		// Create tag
		var courseItemTag = document.createElement('p');
		courseItemTag.innerHTML = createCourseItemString(courseItems, i);
		courseItemTag.id = courseID; // id is the courseID
		courseItemTag.class = courseItems[i].courseItemId;
		courseItemTag.addEventListener("click", populateCourseItemDescription);

		// Append to div
		courseItemDiv.appendChild(courseItemTag);
	}
}

// Mostly just copy and pasted, logic should be relooked at
function populateCourseItemDescription(tar) {
	var courseID = tar.target.id;
	var courseItemID = tar.target.class;
	var courseItems;
	var courseItemDes = document.getElementById("courseItemDescriptions");

	for (var i in courseItemJSON) {
		if (i == courseID) {
			for (var j in courseItemJSON[i]) {
				if (courseItemJSON[i][j].courseItemId == courseItemID){
					courseItems = courseItemJSON[i][j];
				}
			}
		}
	}
	
	// clear current list
	while (courseItemDes.firstChild) {
   	 	courseItemDes.removeChild(courseItemDes.firstChild);
	}

	for (var i in courseItems) {
		if(i == "courseItemId") {
			continue;
		}
		// Create tag
		var courseItemTag = document.createElement('p');
		courseItemTag.innerHTML = i + ": " + courseItems[i];

		// Append to div
		courseItemDes.appendChild(courseItemTag);
		}

}

// Creates the string for the user
function createCoursesString(courseJSON, i) {
	var term;
	switch ( courseJSON[i][0].term) {
		case 0: 
			term = "Fall";
			break;
		case 1:
			term = "Spring"
			break;
		case 2:
			term = "Summer"
			break;
		default:
			console.log("invalid term number: " + term);
	}

	return courseJSON[i][0].department + " " + courseJSON[i][0].courseNumber + " " + courseJSON[i][0].course + " (" + courseJSON[i][0].year + " " + term + ")";
}

function createCourseItemString(courseItem, i) {
	return courseItem[i].name;
}

// function teCourseItemDescriptionString(courseItems, i) {
// 	return courseItem[i].name;
// }
