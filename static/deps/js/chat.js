users = [];
messages = [];

var chat_target = JSON.parse(
  document.getElementById("target-user").textContent
);

if (chat_target) {
  document.getElementById("chat-header-name").textContent = chat_target;
}

var current_user = JSON.parse(
  document.getElementById("current-user").textContent
);

function updateContactsList(usernames) {
  $("#contacts-list").empty();
  for (var i = 0; i < usernames.length; i++) {
    if (usernames[i] != current_user) {
      var username = usernames[i];
      $("#contacts-list").append(
        `<a id="${username}" href="/chat/${username}" class="list-group-item list-group-item-action d-flex align-items-center">` +
          '<div class="d-flex flex-column">' +
          '<h6 class="mb-1">' +
          username +
          "</h6>" +
          "</div>" +
          '<span class="badge badge-primary badge-pill ml-auto">2</span>' +
          "</a>"
      );
    }
  }

  if (chat_target) {
    var currentUrl = window.location.href;

    if (currentUrl.includes(chat_target)) {
      document.querySelector(`#${chat_target}`).classList.add("active");
    }

    document.querySelector(`#${chat_target}`).onclick = function (e) {
      document.querySelector(`#${chat_target}`).classList.add("active");
    };
  }
}

function drawInMessage(message, time) {
  var date = new Date(time); // преобразование строки времени в объект Date
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var formattedTime =
    (hours < 10 ? "0" : "") + hours + ":" + (minutes < 10 ? "0" : "") + minutes; // форматирование времени в формат HH:MM
  $("#chat-messages").append(
    '<div class="d-flex align-items-end mt-2 chatroom">' +
      '<small class="text-muted mr-2">' +
      formattedTime +
      "</small>" +
      '<div class="bg-white rounded p-2">' +
      '<p class="mb-0">' +
      message +
      "</p>" +
      "</div>" +
      "</div>"
  );
}

function drawOutMessage(message, time) {
  var date = new Date(time); // преобразование строки времени в объект Date
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var formattedTime =
    (hours < 10 ? "0" : "") + hours + ":" + (minutes < 10 ? "0" : "") + minutes; // форматирование времени в формат HH:MM
  console.log(formattedTime, message);
  $("#chat-messages").append(
    '<div class="d-flex align-items-end mt-2 ml-auto">' +
      '<small class="text-muted mr-2">' +
      formattedTime +
      "</small>" +
      '<div class="bg-white rounded p-2">' +
      '<p class="mb-0">' +
      message +
      "</p>" +
      "</div>" +
      "</div>"
  );
}

function drawMessages(messages) {
  current_chat_messages = messages[chat_target];
  // console.log(current_chat_messages);
  for (var i = 0; i < current_chat_messages.length; i++) {
    var message = current_chat_messages[i];
    console.log(message);
    if (message.sender === current_user) {
      // console.log(message.sender, message.text, message.created_at);
      drawOutMessage(message.text, message.created_at);
    }
    if (message.receiver === current_user) {
      drawInMessage(message.text, message.created_at);
    }
  }
}

// var message_check = "";

function saveMessages(messages) {
  var messagesByRoom = {};
  for (var i = 0; i < messages.length; i++) {
    var message = messages[i];
    var room =
      message.sender === current_user ? message.receiver : message.sender;
    if (messagesByRoom[room]) {
      messagesByRoom[room].push(message);
    } else {
      messagesByRoom[room] = [message];
    }
  }
  return messagesByRoom;
}

function connectSocket() {
  const chatSocketURL =
    "ws://" +
    window.location.host +
    "/ws/chat/" +
    (chat_target ? chat_target + "/" : "");

  const chatSocket = new WebSocket(chatSocketURL);

  chatSocket.onmessage = function (event) {
    let data = JSON.parse(event.data);
    // console.log(data);
    switch (data.type) {
      case "users_list":
        users = data.usernames;
        updateContactsList(users);
        break;
      case "user_joined":
        if (!users.includes(data.username)) {
          users.push(data.username);
          updateContactsList(users);
        }
        break;
      case "user_left":
        const index = users.indexOf(data.username);
        if (index > -1) {
          users.splice(index, 1);
          updateContactsList(users);
        }
        break;
      case "messages_list":
        var formatted_messages = saveMessages(data.messages);
        // console.log(formatted_messages);
        drawMessages(formatted_messages);
        // console.log(saveMessages(messages));
        break;
      case "message":
        messages.push(data);
        break;
      default:
        break;
    }
  };

  chatSocket.onclose = function (e) {
    console.error("Chat socket closed unexpectedly");
  };

  document.querySelector("#chat-message-input").onkeyup = function (e) {
    if (e.key === "Enter") {
      document.querySelector("#chat-message-submit").click();
    }
  };

  document.querySelector("#chat-message-submit").onclick = function (e) {
    const messageInputDom = document.querySelector("#chat-message-input");
    const message = messageInputDom.value;
    console.log("Sending message: " + message);
    chatSocket.send(
      JSON.stringify({
        "message": message,
      })
    );
    messageInputDom.value = "";
  };
}

connectSocket();
