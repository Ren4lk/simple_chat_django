let users = [];
let selectedUsername;
let formattedMessages = {};

const currentUser = JSON.parse(
  document.getElementById("current-user").textContent
);

let genderFilter = "all";
let searchQuery = "";

function drawMessage(message, time, isOutgoing) {
  const date = new Date(time);
  const formattedTime = date.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });

  const messageHTML = `
    <div class="d-flex align-items-end mt-2 ${
      isOutgoing ? "ml-auto" : "chatroom"
    }">
      <small class="text-muted mr-2">${formattedTime}</small>
      <div class="bg-white rounded p-2">
        <p class="mb-0">${message}</p>
      </div>
    </div>`;

  const chatMessages = $("#chat-messages");
  chatMessages.append(messageHTML);

  const chatContainer = chatMessages.parent();
  chatContainer.scrollTop(chatContainer.prop("scrollHeight"));
}

function drawIncomingMessage(message, time) {
  drawMessage(message, time, false);
}

function drawOutgoingMessage(message, time) {
  drawMessage(message, time, true);
}

function drawAllMessages(messages) {
  $("#chat-messages").empty();
  messages.forEach((message) => {
    if (message.sender === currentUser.username) {
      drawOutgoingMessage(message.text, message.created_at);
    } else {
      drawIncomingMessage(message.text, message.created_at);
    }
  });
}

function parseMessages(messages) {
  return messages.reduce((messagesByRoom, message) => {
    const room =
      message.sender === currentUser.username
        ? message.receiver
        : message.sender;
    if (!messagesByRoom[room]) {
      messagesByRoom[room] = [];
    }
    messagesByRoom[room].push(message);
    messagesByRoom[room].sort(
      (a, b) => new Date(a.created_at) - new Date(b.created_at)
    );
    return messagesByRoom;
  }, {});
}

function openChat(username) {
  if (username) {
    $(`#id-${username}`).addClass("active");
    $("#chat-message-input").focus();
    $("#chat-header-name").text(username);
    drawAllMessages(formattedMessages[username]);
  }
}

function closeChat() {
  $(`#id-${selectedUsername}`).removeClass("active");
  $("#chat-messages").empty();
  selectedUsername = null;
  $("#chat-header-name").text("Here will be name of chat");
}

$("#contacts-list, #modal-contacts-list").on("click", "a", function (e) {
  if (selectedUsername) {
    closeChat();
  }

  selectedUsername = e.currentTarget.id.split("-").pop();

  openChat(selectedUsername);
  $("#modal-users-window").modal("hide");
});

document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeChat();
  }
});

function addUser(user) {
  if (
    user.username !== currentUser.username &&
    !users.some((u) => u.username === user.username)
  ) {
    users.push(user);
    displayUser(user);
  }
}

function removeUser(user) {
  users = users.filter((u) => u.username !== user.username);
  unDisplayUser(user);
}

function displayUser(user) {
  if (
    (genderFilter === "all" || user.gender === genderFilter) &&
    user.username.toLowerCase().includes(searchQuery)
  ) {
    if (!$(`#id-${user.username}`).length) {
      const userHTML = `
        <a id="id-${
          user.username
        }" class="list-group-item list-group-item-action d-flex align-items-center ${
        user.username === selectedUsername ? "active" : ""
      }">
          <div class="d-flex flex-column">
            <h6 class="mb-1">${user.username}</h6>
          </div>
          <span class="badge badge-primary badge-pill ml-auto">${user.language.toUpperCase()}</span>
        </a>`;
      $("#contacts-list").append(userHTML);
      $("#modal-contacts-list").append(userHTML.replace("id-", "id-modal-"));
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

$("#user-search, #modal-search-input").on("input", function () {
  searchQuery = $(this).val().toLowerCase();
  updateDisplayedUsers();
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
  PING_INTERVAL = 5000;

  chatSocket.onopen = function (e) {
    console.log("Successfully connected to the WebSocket.");
  };

  chatSocket.onclose = function (e) {
    console.log(
      "WebSocket connection closed unexpectedly. Trying to reconnect in 2s..."
    );
    setTimeout(function () {
      console.log("Reconnecting...");
      connectSocket();
    }, 2000);
  };

  chatSocket.onmessage = function (event) {
    let data;
    try {
      data = JSON.parse(event.data);
    } catch (err) {
      console.error("Unexpected error when parsing WebSocket message:", err);
      return;
    }
    console.log(data);
    switch (data.type) {
      case "users_list":
        data.users.forEach(addUser);
        break;
      case "user_joined":
        addUser(data.user);
        break;
      case "user_left":
        removeUser(data.user);
        break;
      case "messages_list":
        formattedMessages = parseMessages(data.messages);
        break;
      case "chat_message":
        if (!formattedMessages[data.message.sender]) {
          formattedMessages[data.message.sender] = [];
        }
        formattedMessages[data.message.sender].push(data.message);
        if (data.message.sender === selectedUsername) {
          drawIncomingMessage(data.message.text, data.message.created_at);
        }
        break;
      case "chat_message_delivered":
        if (!formattedMessages[data.message.receiver]) {
          formattedMessages[data.message.receiver] = [];
        }
        formattedMessages[data.message.receiver].push(data.message);
        if (data.message.receiver === selectedUsername) {
          drawOutgoingMessage(data.message.text, data.message.created_at);
        }
        break;
      default:
        break;
    }
  };

  chatSocket.onerror = function (err) {
    console.log("WebSocket encountered an error: " + err.message);
    console.log("Closing the socket.");
    chatSocket.close();
  };

  setInterval(() => {
    chatSocket.send(JSON.stringify({ "type": "ping" }));
  }, PING_INTERVAL);

  document.querySelector("#chat-message-input").onkeyup = function (e) {
    if (e.key === "Enter") {
      document.querySelector("#chat-message-submit").click();
    }
  };

  document.querySelector("#chat-message-submit").onclick = function (e) {
    const messageInputDom = document.querySelector("#chat-message-input");
    const message = messageInputDom.value.trim();

    if (message) {
      chatSocket.send(
        JSON.stringify({
          "message": message,
          "target_user": selectedUsername,
        })
      );
      messageInputDom.value = "";
    } else {
      console.log("Input message cannot be empty.");
    }
  };
}

connectSocket();
