$(function() {
  /*
        TODO:
    */

  //   Globals

  selectedCourses = [];
  courseSections = {}; // stores courses as keys and theirs sections' ids in array.
  //{'CSC111':['A01','B01']}

  // Cashing input fields
  $term = $("#term");
  $cName = $("#cName");
  $cNum = $("#cNum");

  $Mstart = $("#Mstart");
  $Tstart = $("#Tstart");
  $Wstart = $("#Wstart");
  $Rstart = $("#Rstart");
  $Fstart = $("#Fstart");

  $Mend = $("#Mend");
  $Tend = $("#Tend");
  $Wend = $("#Wend");
  $Rend = $("#Rend");
  $Fend = $("#Fend");

  //Cashing course-info window and tables window
  $cInfo = $("#cInfo");
  $tables = $("#tables");
  $messages = $("#messages");

  // Events listeners

  //Reset button
  $("#reset").on("click", function() {
    $term.val("201901");
    $cName.val("AGEI");
    $cNum.val("");

    $Mstart.val(0).trigger("input");
    $Tstart.val(0).trigger("input");
    $Wstart.val(0).trigger("input");
    $Rstart.val(0).trigger("input");
    $Fstart.val(0).trigger("input");

    $Mend.val(24).trigger("input");
    $Tend.val(24).trigger("input");
    $Wend.val(24).trigger("input");
    $Rend.val(24).trigger("input");
    $Fend.val(24).trigger("input");

    removeErrors();
  });

  // Range sliders, start vs end are consistent
  $(".dayTime-slider.start").on("input", function() {
    //get relative end slider
    var $end = $(
      "#" +
        $(this)
          .attr("id")
          .substr(0, 1) +
        "end"
    );

    // if less put it equal
    if (parseInt($(this).val()) > parseInt($end.val())) {
      $end.val($(this).val()).trigger("input");
    }
  });

  $(".dayTime-slider.end").on("input", function() {
    //get relative start slider
    var $start = $(
      "#" +
        $(this)
          .attr("id")
          .substr(0, 1) +
        "start"
    );

    // if more put it equal
    if (parseInt($(this).val()) < parseInt($start.val())) {
      $start.val($(this).val()).trigger("input");
    }
  });

  // Select course and put in tabs
  $("#select-course").on("click", function() {
    removeErrors();

    // check if course is already there
    var alreadyIn = selectedCourses.reduce((prev, curr) => {
      return prev || ($cName.val() === curr[0] && $cNum.val() === curr[1]);
    }, false);

    // Validate and send
    if (!$cNum.val()) {
      postError("numNotGiven");
    } else if (100 > parseInt($cNum.val()) || parseInt($cNum.val()) >= 800) {
      postError("invalidNum");
    } else if (alreadyIn) {
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
          selectedCourses.push([$cName.val(), $cNum.val()]);
          courseSections[data.course.replace(" ", "")] = data.sections;
          addTab($cInfo, data.course, data.html);
        },
        error: data => {
          postError("connection-error");
        }
      });
    }
  });

  // Helper functions

  // adds tab
  function addTab($tabPanels, header, content) {
    // create
    var $tab = $("<li></li>")
      .text(header)
      .attr({
        rel: header.replace(" ", "-")
      })
      .on("click", ToggleTab);

    // add close button
    $tab.append(
      $("<span>")
        .addClass("close")
        .on("click", closeTab)
    );

    // add tab
    $tabPanels.find(".tabs").append($tab);

    var $panel = $("<div></div>")
      .addClass("panel")
      .attr({
        id: header.replace(" ", "-")
      })
      .html(content);

    //create and add panel
    $tabPanels.append($panel);

    //select this tab
    $tab.click();
  }

  // changes tabs when clicked
  function ToggleTab() {
    var $panel = $(this).closest(".tab-panels");

    $panel.find(".tabs li.active").removeClass("active");
    $(this).addClass("active");

    //figure out which panel to show
    var panelToShow = $(this).attr("rel");

    //hide current panel if exists (might not at start)
    var $activePanel = $panel.find(".panel.active");

    if ($activePanel[0]) {
      $activePanel.hide(0, showNextPanel);
    } else {
      showNextPanel();
    }

    //show next panel
    function showNextPanel() {
      $(this).removeClass("active");

      $("#" + panelToShow).show(0, function() {
        $(this).addClass("active");
      });
    }
  }

  // closes tabs when clicked close
  function closeTab() {
    var $tab = $(this).closest("li");

    // remove from seleced courses (if from $cinfo)
    if (
      $tab
        .parent()
        .parent()
        .is($cInfo)
    ) {
      var course = $tab.attr("rel").split("-");
      var index = selectedCourses.findIndex(e => {
        return e[0] === course[0] && e[1] === course[1];
      });
      if (index !== -1) selectedCourses.splice(index, 1);
    }

    // show another tab if tab was active
    if ($tab.hasClass("active")) {
      if ($tab.next()[0]) {
        $tab.next().trigger("click");
      } else {
        $tab.prev().trigger("click");
      }
    }

    $("#" + $tab.attr("rel")).remove();
    $tab.remove();
  }

  //post error message
  function postError(error) {
    // create message, marked with error (class alreadyIn)
    var $message = $("<li>")
      .css({
        color: "red"
      })
      .addClass(error);

    switch (error) {
      case "alreadyIn":
        $message.text("Course already selected");
        break;

      case "invalidNum":
        $message.text("No. is invalid");
        break;

      case "numNotGiven":
        $message.text("No. not given");
        break;

      case "connection-error":
        $message.text("Error Ocurred in connecting to back-end");
    }

    //Post it to user
    $messages.append($message);
  }

  //removes error messages to user
  function removeErrors() {
    $(".alreadyIn").remove();
    $(".invalidNum").remove();
    $(".numNotGiven").remove();
    $(".connection-error").remove();
  }
});
