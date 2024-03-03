function updateContactsList(contacts) {
  $("#contacts-list").empty();
  for (var i = 0; i < contacts.length; i++) {
    var contact = contacts[i];
    $("#contacts-list").append(
      '<a href="#" class="list-group-item list-group-item-action d-flex align-items-center">' +
        '<div class="d-flex flex-column">' +
        '<h6 class="mb-1">' +
        contact.username +
        "</h6>" +
        "</div>" +
        '<span class="badge badge-primary badge-pill ml-auto">2</span>' +
        "</a>"
    );
  }
}

var csrfToken = $("[name=csrfmiddlewaretoken]").val();

function ajaxRequestContacts() {
  $.ajax({
    method: "POST",
    url: "/chat/update-contacts/",
    beforeSend: function (xhr) {
      xhr.setRequestHeader("X-CSRFToken", csrfToken);
    },
    success: function (data) {
      updateContactsList(data.contacts);
      csrfToken = data.csrfmiddlewaretoken;
      $("[name=csrfmiddlewaretoken]").val(csrfToken);
    },
    error: function () {
      console.log("Ошибка при выполнении AJAX-запроса");
    },
  });
}

$(document).ready(function () {
  contacts_update_url = $(this).attr("href");

  let error_form_message = document.querySelector("#non_field_errors");

  if (error_form_message) {
    setTimeout(function () {
      error_form_message.style.opacity = "0";
    }, 4000);
  }

  if (window.location.pathname.includes("/chat/")) {
    ajaxRequestContacts();
    setInterval(ajaxRequestContacts, 10000);
  }
});
