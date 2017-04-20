var myFirebaseRef = firebase.database().ref();
var myFirebase;
var usernameInput = document.querySelector('#WelcomeMessage');
var textInput = document.querySelector('#chattext');
var postButton = document.querySelector('#chatpost');
var courses = [];

$(textInput).bind('keypress',pressed);

getCourses();
attachListener();

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

	var addClass = "highlight2";
	var courseItems = document.getElementById("courseItems");
	var children = courseItems.children;

	for (var i = children.length - 1; i >= 0; i--) {
  		var child = children[i];
  		$(child).removeClass(addClass);
	}

	$(this).addClass(addClass);


	var currentCourse = document.getElementsByClassName("highlight");
	// Change DB Ref
	myFirebase = myFirebaseRef.child(currentCourse[0].innerHTML + this.class + " " + this.innerHTML);

	// clear current list
	var chatresults = document.getElementById("chatresults");
	while (chatresults.firstChild) {
   	 	chatresults.removeChild(chatresults.firstChild);
	}

	// Attach on child added
	myFirebase.off();
	attachListener();
	// myFirebase.on('child_added', function(snapshot) {
	// 	var msg = snapshot.val();

		

	// 	var msgUsernameElement = document.createElement("b");
	// 	msgUsernameElement.textContent = msg.username;

	// 	var msgTextElement = document.createElement("p");
	// 	msgTextElement.textContent = msg.text;

	// 	var msgElement = document.createElement("div");
	// 	var msgUser = usernameInput.innerHTML;
 //  		var userName = splitUsername(msgUser);
	// 	if (msg.username == userName) {
	// 		// This users text (push it left)
	// 		$(msgElement).css("position", "relative");
	// 		$(msgElement).css("left", "300px");

	// 	}
	// 	msgElement.appendChild(msgUsernameElement);
	// 	msgElement.appendChild(msgTextElement);

	// 	document.getElementById("chatresults").appendChild(msgElement);
	// });
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
	myFirebase.off();
	attachListener();
	// console.log("events");
	// console.log($(myFirebase).data('events'));
	// myFirebase.on('child_added', function(snapshot) {
	// 	var msg = snapshot.val();

	// 	var msgUsernameElement = document.createElement("b");
	// 	msgUsernameElement.textContent = msg.username;

	// 	var msgTextElement = document.createElement("p");
	// 	msgTextElement.textContent = msg.text;

	// 	var msgElement = document.createElement("div");
	// 	var msgUser = usernameInput.innerHTML;
 //  		var userName = splitUsername(msgUser);
	// 	if (msg.username == userName) {
	// 		// This users text (push it left)
	// 		$(msgElement).css("position", "relative");
	// 		$(msgElement).css("left", "300px");

	// 	}
	// 	msgElement.appendChild(msgUsernameElement);
	// 	msgElement.appendChild(msgTextElement);

	// 	document.getElementById("chatresults").appendChild(msgElement);
	// });
}

postButton.addEventListener("click", function() {
	if(textInput.value == "") {
		// do nothing
	}
	else {
		var msgUser = usernameInput.innerHTML;
	  	var userName = splitUsername(msgUser)
	 	var msgText = textInput.value;
	  	myFirebase.push({username:userName, text:msgText});
	  	textInput.value = "";
	}
  	
});

function pressed(e)
{
	 if(e.keyCode === 13) {
	 	if(textInput.value == "") {
		// do nothing
		}
		else {
			var msgUser = usernameInput.innerHTML;
		  	var userName = splitUsername(msgUser)
		 	var msgText = textInput.value;
		  	myFirebase.push({username:userName, text:msgText});
		  	textInput.value = "";
		}
	}
}

function splitUsername(username) {
	return username.substring(username.indexOf("welcome") + 8, username.indexOf("<") - 2);
}

function attachListener() {

	myFirebase.on('child_added', function(snapshot) {
		var msg = snapshot.val();

		var msgUsernameElement = document.createElement("div");

		msgUsernameElement.innerHTML = msg.username.substring(0, msg.username.indexOf('@'));
		msgUsernameElement.class = "name";
		$(msgUsernameElement).css("position", "relative");
		$(msgUsernameElement).css("left", "10px");
		$(msgUsernameElement).css("color", "#3366ff");

		var msgTextElement = document.createElement("div");
		msgTextElement.innerHTML = msg.text;
		msgTextElement.class = "message";
		$(msgTextElement).css("position", "relative");
		$(msgTextElement).css("left", "30px");

		var msgElement = document.createElement("div");
		$(msgElement).addClass("message-container");
		$(msgElement).addClass("visible");

		var msgUser = usernameInput.innerHTML;
		var userName = splitUsername(msgUser);

		if (msg.username == userName) {
			// This users text (push it left)
			$(msgUsernameElement).css("left", "350px");
			$(msgTextElement).css("left", "360px");


		}
		else {
			// Not users text (push it slightly left)
			//$(msgElement).css("left", "10px");
		}
		msgElement.appendChild(msgUsernameElement);
		msgElement.appendChild(msgTextElement);

		document.getElementById("chatresults").appendChild(msgElement);
	});
}