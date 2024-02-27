$(document).ready(function () {

    contacts_update_url = $(this).attr("href");

  $.ajax({
    method: "POST",
    url: "/chat/update-contacts/",
    data: {
      csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
    },
    success: function (data) {
      updateContactsList(data.contacts);
    },
    error: function () {
      console.log("Ошибка при выполнении AJAX-запроса");
    },
  });

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
});
