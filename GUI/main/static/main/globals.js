$(function () {

    // Globals
    selectedCourses = [];
    courseSections = {}; // stores courses as keys and theirs sections' ids in array.
    //{'CSC111':['A01','B01']}

    $term = $("#term")
    $cName = $("#cName")
    $cNum = $("#cNum")

    // sliders
    start = {
        $M: $("#Mstart"),
        $T: $("#Tstart"),
        $W: $("#Wstart"),
        $R: $("#Rstart"),
        $F: $("#Fstart")
    }

    end = {
        $M: $("#Mend"),
        $T: $("#Tend"),
        $W: $("#Wend"),
        $R: $("#Rend"),
        $F: $("#Fend")
    }

    //Cashing course-info window and tables window
    $cInfo = $("#cInfo");
    $tables = $("#tables");
    $messages = $("#messages");
});
