var myFirebase = firebase.database().ref();
var usernameInput = document.querySelector('#WelcomeMessage');
var textInput = document.querySelector('#chattext');
var postButton = document.querySelector('#chatpost');

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