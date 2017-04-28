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
		var d = new Date()
		console.log(d)
		var msg = snapshot.val();

		var msgUsernameElement = document.createElement("p");

		msgUsernameElement.innerHTML = msg.username.substring(0, msg.username.indexOf('@'));
		msgUsernameElement.class = "name";

		var msgTextElement = document.createElement("p");
		msgTextElement.innerHTML = msg.text;
		msgTextElement.class = "message";


		var msgElement = document.createElement("div");
		$(msgElement).addClass("container-fluid");
		$(msgElement).addClass("visible");

		$(msgElement).addClass("col-md-12");

		var row1 = document.createElement("div");
		$(row1).addClass("row");
		msgElement.appendChild(row1)

		$(msgUsernameElement).addClass("chat_text");
		$(msgUsernameElement).addClass("chat_username");
		$(msgTextElement).addClass("chat_text");

		var msgUser = usernameInput.innerHTML;
		var userName = splitUsername(msgUser);

		var p_container = document.createElement("div");
		var p_container2 = document.createElement("div");
		$(p_container).addClass("col-md-12");
		$(p_container2).addClass("col-md-12");


		row1.appendChild(p_container);
		row1.appendChild(p_container2);

		p_container.appendChild(msgUsernameElement);
		p_container2.appendChild(msgTextElement);

		if (msg.username == userName) {
			$(p_container).addClass("row1");
			$(p_container2).addClass("row2");
			// This users text (push it left)
			$(msgUsernameElement).css("float", "right");
			$(msgTextElement).css("float", "right");
			// $(msgTextElement).parent().closest('div').css("float", "right");


		}
		else {}
		

		document.getElementById("chatresults").appendChild(msgElement);
	});
}