$(function () {

    // Range sliders, start vs end are consistent
    $(".dayTime-slider.start").on("input", function () {
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

    $(".dayTime-slider.end").on("input", function () {
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
});
