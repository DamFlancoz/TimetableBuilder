$(function () {
  /**
   * @fileoverview All event listeners are added here
   */

  /**
   * Selects inputted course and displays it in a tab in cInfo panel.
   */
  $("#select-course").on("click", function () {
    removeErrors();

    // Validate and send
    if (!$cNum.val()) {
      postError("numNotGiven");
    } else if (100 > parseInt($cNum.val()) || parseInt($cNum.val()) >= 800) {
      postError("invalidNum");
    } else if (courseAlreadySelected()) {
      postError("alreadyIn");
    } else {
      $.ajax({
        type: "GET",
        url: "/api/cInfo/",
        data: {
          term: parseInt($term.val()),
          cName: $cName.val(),
          cNum: parseInt($cNum.val())
        },
        success: data => {
          selectedCourses.push(new Course($cName.val(), $cNum.val()));
          //TODO cash the radio buttons
          addCInfoTab($cInfo, data.course, data.html);
        },
        error: data => {
          postError("connection-error");
        }
      });
    }
  });
});
