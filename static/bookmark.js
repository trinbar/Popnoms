// Document ready prevents JS from loading until all HTML has loaded

function showBookmarkSuccess(results) {
  $("#bookmark_success").html(results);
  $("#bookmarksuccess").show();
  setTimeout(function () {$("#bookmark_success").hide();} , 3000);

}

$(document).ready(
    function() {
    $(".bookmark").on("click", function(evt) {
      let eventId = $(this).data("data-eventid");
      let bookmarkType = $(this).data("data-status");
      let payload = {"event_id": eventId,
                   "bookmark_type": bookmarkType};

      $.post("/bookmark_event", payload, showBookmarkSuccess);
    });

    


});