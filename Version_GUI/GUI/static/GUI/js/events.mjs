
/**
 * @fileoverview All event listeners are added here
 */


import { courseAlreadySelected } from './helper.mjs';
import { addTab } from './tabs.mjs';
import { removeErrors, postError } from './messages.mjs';

$(function () {
  removeErrors();

  function refreshTable() {
    removeErrors();

    $.ajax({
      type: "POST",
      url: "/api/table/",
      data: {
        term: parseInt($term.val()),

        // Makes mapping like {<course>:{'lab':<lab section>,...} ... more courses}
        selectedSections: JSON.stringify(selectedCourses.reduce((obj, course) => {
          obj[course.toString()] = {
            'lab': course.getLab(),
            'lecture': course.getLecture(),
            'tutorial': course.getTutorial(),
          };
          return obj;
        }, {})),

      },
      success: data => {
        if (data.error === "None") {
          $table.html(data.tableHTML);
        } else {
          postError(data.error);
        }
      },
      error: () => {
        postError("connection-error");
      }
    })
  }

  /**
   * Selects inputted course and displays it in a tab in cInfo panel.
   */
  $("#select-course").on("click", function () {
    removeErrors();

    // Validate and send
    if (!$cNum.val()) {
      postError("num-not-given");

    } else if (!(/^\d{3}$/.exec($cNum.val())) || 100 > parseInt($cNum.val()) || parseInt($cNum.val()) >= 800) {
      postError("invalid-num");

    } else if (courseAlreadySelected()) {
      postError("already-in");

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

          var course = new Course($cName.val(), $cNum.val())
          selectedCourses.push(course);


          // Init The course Tab
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


          course.$panel = $cInfo.find(`#${course.name}-${course.num}`);
          course.$panel.find("input").on("click", refreshTable);
        },
        error: () => {
          postError("connection-error");
        }
      });
    }
  });
});
