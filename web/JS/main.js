window.setTimeout(setUp, 500);

function validateDocumentUploadForm(){
	var courseItemID = document.getElementById("courseitemid").value
	if(courseItemID == null || courseItemID == ""){
		alert("Please click on Course Item that this document is related to and then upload.")
		return false;
	}
}

function validateForm() {
	var name = document.getElementById("assignmentName").value;
	var description = document.getElementById("assignmentDescription").value;
	var assignDate = document.getElementById("assignDate").value;
	var dueDate = document.getElementById("dueDate").value;
	var courseItems = document.getElementById("courseItems").children;
	for(var i =0; i<courseItems.length; i++){
		if(courseItems[i].innerHTML == name){
			alert("Course Item name already exists, please change it");
	    	return false;
		}
	}
	if (name == null || name=="" || description==null || description=="") {
		alert("Please Fill All Required Field");
	    return false;
	}
    else if (!Date.parse(assignDate) || !Date.parse(dueDate)) {
		alert("Please Fill All Required Field");
	    return false;
   	}
   	else {

    	return true;
   	}
}

function setUp () {
	var x = document.getElementById("courses");
	if (x.firstElementChild) {
		x.firstElementChild.click();
	}

}

function openCourseItems(courseID, course_item_list){

	var elements = document.getElementsByClassName('courseItemDescription');
	var elements2 = document.getElementById('documents')
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
    while (elements2.firstChild) {
   	 	elements2.removeChild(elements2.firstChild);
	}



	course = document.getElementById(courseID);

	var addClass = "highlight";

	$(".courses").removeClass(addClass);
	$("#" + courseID).addClass(addClass);

	course_items = course_item_list[courseID];
	
	var correctedJSON;

	populateCourseItems(courseID,course_item_list);

}

function populateCourses(courseJSON) {
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


function populateCourseItems(aCourseID, courseItemJSON) {
	var courseID = aCourseID
	document.getElementById('courseid').value = courseID;
	var courseItems;
	var courseItemDiv = document.getElementById("courseItems");

	for (var i in courseItemJSON) {
		if (i == courseID) {
			courseItems = courseItemJSON[i];
			break;
		}
	}
	
	while (courseItemDiv.firstChild) {
   	 	courseItemDiv.removeChild(courseItemDiv.firstChild);
	}

	for (var i in courseItems) {
		var correctedJSON = JSON.parse(courseItems[i]);
		// Create tag
		var courseItemID = 0;
		var courseItemTag = document.createElement('p');
		courseItemTag.innerHTML = correctedJSON.Name
		courseItemTag.id = courseID; // id is the courseID
		courseItemTag.class = correctedJSON.courseItemId;
		

		// Append to div
		courseItemDiv.appendChild(courseItemTag);

		courseItemID = correctedJSON.courseItemId;

		(function(_courseItemID) {
			courseItemTag.addEventListener("click", function(){populateCourseItemDescription(courseID, courseItemJSON, _courseItemID)});	
		})(courseItemID);

		(function(_courseItemID) {
			courseItemTag.addEventListener("click", function(){populateDocuments(courseID, courseItemJSON, _courseItemID)});	
		})(courseItemID);
		
	}

	// Function in chat
	getCourseItems();
}

function populateDocuments(courseID, courseItemJSON, aCourseItemID){
	var courseID = courseID
	var courseItemID = aCourseItemID
	var courseItems;
	var courseItemDes = document.getElementById("documents");
	document.getElementById("courseitemid").value = courseItemID;

	for (var i in courseItemJSON) {
		if (i == courseID) {
			for (var j in courseItemJSON[i]) {
				var prettyjson = JSON.parse(courseItemJSON[i][j])
				if (prettyjson.courseItemId == courseItemID){
					courseItems = prettyjson;
					break;
				}

			}
			break;
		}
	}
	
	// clear current list
	while (courseItemDes.firstChild) {
   	 	courseItemDes.removeChild(courseItemDes.firstChild);
	}


	var assignmentname = courseItems.name

	for (var i in courseItems) {
		if(i == "documents"){
			var k = 1;
			for (var j in courseItems[i]){
				var res = courseItems[i][j].split(":");
				var courseItemTag = document.createElement('p');
				courseItemTag.className += "documents"
				courseItemTag.innerHTML = courseItems[i]
				var link = document.createElement('a');
				link.textContent = res[0];
				link.href = '/upload_view_document/' + res[1];
				link.style.paddingRight = "20px";
				courseItemDes.appendChild(link);
				var user = document.getElementById("nickname").value
				var usersplit= user.split("@")
				if(res.length == 3){

					if(res[2] == usersplit[0]){
						var btn = document.createElement("button");
						var t = document.createTextNode("Remove");
						var cid = document.getElementById("courseitemid").value
						btn.appendChild(t); 
						courseItemDes.appendChild(btn); 
						btn.onclick = function () {
							var form = document.createElement('form');
    						form.setAttribute('method', 'post');
   							form.setAttribute('action', "/upload_remove_document/" + res[1]+":"+cid);
   							form.style.display = 'hidden';
    						document.body.appendChild(form)
    						form.submit();
						};
					}
				}
				linebreak = document.createElement("br")
				courseItemDes.appendChild(linebreak)
				k= k+1
			}




		}
		}

}

// Mostly just copy and pasted, logic should be relooked at
function populateCourseItemDescription(aCourseID, courseItemJSON, aCourseItemID) {

	var courseID = aCourseID
	var courseItemID = aCourseItemID
	var courseItems;
	var courseItemDes = document.getElementById("courseItemDescriptions");
	document.getElementById("courseitemid").value = courseItemID;

	for (var i in courseItemJSON) {
		if (i == courseID) {
			for (var j in courseItemJSON[i]) {
				var prettyjson = JSON.parse(courseItemJSON[i][j])
				if (prettyjson.courseItemId == courseItemID){
					courseItems = prettyjson;
					break;
				}

			}
			break;
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
		if(i == "documents"){
			continue;
		}
		// Create tag
		var courseItemTag = document.createElement('p');
		courseItemTag.innerHTML = i + ": " + courseItems[i];
		courseItemTag.className += "courseItemDescription"
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
