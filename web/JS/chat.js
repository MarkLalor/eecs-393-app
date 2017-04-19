var myFirebaseRef = firebase.database().ref();
var myFirebase;
var usernameInput = document.querySelector('#WelcomeMessage');
var textInput = document.querySelector('#chattext');
var postButton = document.querySelector('#chatpost');
var courses = [];


getCourses();


function getCourses() {
	courses = document.getElementsByClassName("courses");
	for (var i in courses) {
		var course = courses[i];
		if (course != undefined && course.tagName != undefined && course.tagName == "P"){
			course.addEventListener('click', handleCourseDBCHange);
		}
	}
	myFirebase = myFirebaseRef.child(courses[0].innerHTML);
}

function getCourseItems() {
	var courseItems = document.getElementById("courseItems");
	var children = courseItems.children;

	for (var i = children.length - 1; i >= 0; i--) {
  		var child = children[i];
  		child.addEventListener('click', handleCourseItemDBCHange);
	}
}

function handleCourseItemDBCHange() {
	var currentCourse = document.getElementsByClassName("highlight");
	// Change DB Ref
	myFirebase = myFirebaseRef.child(currentCourse[0].innerHTML + this.class + " " + this.innerHTML);

	// clear current list
	var chatresults = document.getElementById("chatresults");
	while (chatresults.firstChild) {
   	 	chatresults.removeChild(chatresults.firstChild);
	}

	// Attach on child added
	myFirebase.on('child_added', function(snapshot) {
		var msg = snapshot.val();

		var msgUsernameElement = document.createElement("b");
		msgUsernameElement.textContent = msg.username;

		var msgTextElement = document.createElement("p");
		msgTextElement.textContent = msg.text;

		var msgElement = document.createElement("div");
		msgElement.appendChild(msgUsernameElement);
		msgElement.appendChild(msgTextElement);

		document.getElementById("chatresults").appendChild(msgElement);
	});
}

function handleCourseDBCHange() {

	// Change DB Ref
	myFirebase = myFirebaseRef.child(this.innerHTML);

	// clear current list
	var chatresults = document.getElementById("chatresults");
	while (chatresults.firstChild) {
   	 	chatresults.removeChild(chatresults.firstChild);
	}

	// Attach on child added
	myFirebase.on('child_added', function(snapshot) {
		var msg = snapshot.val();

		var msgUsernameElement = document.createElement("b");
		msgUsernameElement.textContent = msg.username;

		var msgTextElement = document.createElement("p");
		msgTextElement.textContent = msg.text;

		var msgElement = document.createElement("div");
		msgElement.appendChild(msgUsernameElement);
		msgElement.appendChild(msgTextElement);

		document.getElementById("chatresults").appendChild(msgElement);
	});
}

postButton.addEventListener("click", function() {
  	var msgUser = usernameInput.innerHTML;
  	var userName = splitUsername(msgUser)
 	var msgText = textInput.value;
 	console.log(userName);
  	myFirebase.push({username:userName, text:msgText});
  	textInput.value = "";
});

function splitUsername(username) {
	return username.substring(username.indexOf("welcome") + 8, username.indexOf("<") - 2);
}

myFirebase.on('child_added', function(snapshot) {
	var msg = snapshot.val();

	var msgUsernameElement = document.createElement("b");
	msgUsernameElement.textContent = msg.username;

	var msgTextElement = document.createElement("p");
	msgTextElement.textContent = msg.text;

	var msgElement = document.createElement("div");
	msgElement.appendChild(msgUsernameElement);
	msgElement.appendChild(msgTextElement);

	document.getElementById("chatresults").appendChild(msgElement);
});