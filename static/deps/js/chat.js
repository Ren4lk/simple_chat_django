var users = [];
var selected_username;
formatted_messages = {};

var current_user = JSON.parse(
  document.getElementById("current-user").textContent
);

$("#modal-users-window").on("shown.bs.modal", function () {
  $("#all").prop("checked", true);
});
var genderFilter = "all";
var searchQuery = "";
function drawInMessage(message, time) {
  var date = new Date(time);
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var formattedTime =
    (hours < 10 ? "0" : "") + hours + ":" + (minutes < 10 ? "0" : "") + minutes;
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
  var date = new Date(time);
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var formattedTime =
    (hours < 10 ? "0" : "") + hours + ":" + (minutes < 10 ? "0" : "") + minutes;
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
  $("#chat-messages").empty();
  for (var i = 0; i < messages.length; i++) {
    var message = messages[i];
    if (message.sender === current_user.username) {
      drawOutMessage(message.text, message.created_at);
    }
    if (message.receiver === current_user.username) {
      drawInMessage(message.text, message.created_at);
    }
  }
}
function parseMessages(messages) {
  var messagesByRoom = {};
  for (var i = 0; i < messages.length; i++) {
    var message = messages[i];
    var room =
      message.sender === current_user.username
        ? message.receiver
        : message.sender;
    if (messagesByRoom[room]) {
      messagesByRoom[room].push(message);
    } else {
      messagesByRoom[room] = [message];
    }
  }
  for (var room in messagesByRoom) {
    messagesByRoom[room].sort(function (a, b) {
      return new Date(a.created_at) - new Date(b.created_at);
    });
  }
  return messagesByRoom;
}
function openChat(username) {
  if (username) {
    $(`#id-${username}`).addClass("active");
    $("#chat-message-input").focus();
    $("#chat-header-name").text(username);
    drawMessages(formatted_messages[username]);
  }
}

function closeChat() {
  $(`#id-${selected_username}`).removeClass("active");
  $("#chat-messages").empty();
  selected_username = null;
  $("#chat-header-name").text("Here will be name of chat");
}

$("#contacts-list").on("click", "a", function (e) {
  if (selected_username) {
    closeChat();
  }

  selected_username = e.currentTarget.id.split("-")[1];

  openChat(selected_username);
});

$("#modal-contacts-list").on("click", "a", function (e) {
  if (selected_username) {
    closeChat();
  }

  selected_username = e.currentTarget.id.split("-")[2];

  openChat(selected_username);
  $("#modal-users-window").modal("hide");
});

document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeChat();
  }
});

function addUser(user) {
  if (user.username === current_user.username) {
    return;
  }
  if (!users.find((u) => u.username === user.username)) {
    users.push(user);

    displayUser(user);
  }
}

function removeUser(user) {
  if (users.find((u) => u.username === user.username)) {
    users = users.filter((u) => u.username !== user.username);
    unDisplayUser(user);
  }
}

function displayUser(user) {
  if (
    (genderFilter === "all" || user.gender === genderFilter) &&
    user.username.toLowerCase().includes(searchQuery)
  ) {
    if (!$(`#id-${user.username}`).length) {
      $("#contacts-list").append(
        `<a id="id-${user.username}" class="list-group-item list-group-item-action d-flex align-items-center">` +
          '<div class="d-flex flex-column">' +
          '<h6 class="mb-1 unselectable">' +
          user.username +
          "</h6>" +
          "</div>" +
          '<span class="badge badge-primary badge-pill ml-auto">2</span>' +
          "</a>"
      );
      $("#modal-contacts-list").append(
        `<a id="id-modal-${user.username}" class="list-group-item list-group-item-action d-flex align-items-center">` +
          '<div class="d-flex flex-column">' +
          '<h6 class="mb-1">' +
          user.username +
          "</h6>" +
          "</div>" +
          '<span class="badge badge-primary badge-pill ml-auto">2</span>' +
          "</a>"
      );
    }
  }
}

function unDisplayUser(user) {
  $(`#id-${user.username}`).remove();
  $(`#id-modal-${user.username}`).remove();
}

$("input[name='filter']").on("change", function () {
  genderFilter = $(this).val();
  updateDisplayedUsers();
});

$("#user-search").on("input", function () {
  searchQuery = $(this).val().toLowerCase();
  updateDisplayedUsers();
});

$("#modal-search-input").on("input", function () {
  if (document.querySelector("#modal-search-input").value.length === 0) {
    searchQuery = "";
    updateDisplayedUsers();
  }
});

document.querySelector("#modal-search-input").onkeyup = function (e) {
  if (e.key === "Enter") {
    document.querySelector("#modal-search-button").click();
  }
};

document.querySelector("#modal-search-button").onclick = function (e) {
  searchQuery = document.querySelector("#modal-search-input").value;
  updateDisplayedUsers();
};

function removeFilteredUsers() {
  users.forEach(function (user) {
    if (
      !(genderFilter === "all" || user.gender === genderFilter) ||
      !user.username.toLowerCase().includes(searchQuery)
    ) {
      unDisplayUser(user);
    }
  });
}

function updateDisplayedUsers() {
  removeFilteredUsers();
  users.forEach(displayUser);
}

function connectSocket() {
  const chatSocketURL = "ws://" + window.location.host + "/ws/chat/";

  const chatSocket = new WebSocket(chatSocketURL);

  chatSocket.onmessage = function (event) {
    let data = JSON.parse(event.data);
    console.log(data);
    switch (data.type) {
      case "users_list":
        data.users.forEach((user) => {
          addUser(user);
        });
        break;
      case "user_joined":
        addUser(data.user);
        break;
      case "user_left":
        removeUser(data.user);
        break;

      case "messages_list":
        formatted_messages = parseMessages(data.messages);
        break;
      case "chat_message":
        if (!formatted_messages[data.message.sender]) {
          formatted_messages[data.message.sender] = [];
        }
        formatted_messages[data.message.sender].push(data.message);
        if (data.message.sender === selected_username) {
          drawInMessage(data.message.text, data.message.created_at);
        }
        break;
      case "chat_message_delivered":
        if (!formatted_messages[data.message.receiver]) {
          formatted_messages[data.message.receiver] = [];
        }
        formatted_messages[data.message.receiver].push(data.message);
        if (data.message.receiver === selected_username) {
          drawOutMessage(data.message.text, data.message.created_at);
        }
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
    chatSocket.send(
      JSON.stringify({
        "message": message,
        "target_user": selected_username,
      })
    );
    messageInputDom.value = "";
  };
}

connectSocket();
