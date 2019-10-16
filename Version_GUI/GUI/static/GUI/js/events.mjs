
/**
 * @fileoverview All event listeners are added here
 */


import { courseAlreadySelected } from './helper.mjs';
import { addTab } from './tabs.mjs';
import { removeErrors, postError } from './messages.mjs';

$(function () {

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

          function removeFromSelectedCourses() { // close button callback

            var $tab = $(this).closest("li");

            // remove course from selected courses
            var course = $tab.attr("rel").split("-");
            var index = selectedCourses.findIndex(({ name, num }) => {
              return name === course[0] && num === course[1];
            });
            if (index !== -1) selectedCourses.splice(index, 1);
          }

          addTab($cInfo, data.course, data.html, removeFromSelectedCourses);
        },
        error: () => {
          postError("connection-error");
        }
      });
    }
  });
});
