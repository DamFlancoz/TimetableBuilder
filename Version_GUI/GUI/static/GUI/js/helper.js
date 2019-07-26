$(function () {
    /**
     * @fileoverview Contains all functions to help event listeners' definitions.
     */

    /**
     * Checks if the course inputted by user is already selected.
     * @nosideeffects @global
     */
    function courseAlreadySelected() {

        return selectedCourses.reduce((prev, curr) => {
            return prev || ($cName.val() === curr.name && $cNum.val() === curr.num);
        }, false);
    }

    /**
     * Adds a tab for cInfo Panel.
     * @global
     */
    function addCInfoTab($tabPanels, ...args) {
        addTab($tabPanels, ...args, function () {
            $tabPanels.find(".tabs").children().last().find(".close").on("click", closeCInfoTab);
        });
    }

    /**
     * Closes a tab in cInfo Panel. Also takes out the closed course from selectedCourses.
     * @global
     * */
    function closeCInfoTab() {

        closeTab(() => {
            var $tab = $(this).closest("li");

            // remove course from selected courses
            var course = $tab.attr("rel").split("-");
            var index = selectedCourses.findIndex(e => {
                return e[0] === course.name && e[1] === course.num;
            });
            if (index !== -1) selectedCourses.splice(index, 1);
        })
    }

    window.courseAlreadySelected = courseAlreadySelected;
    window.addCInfoTab = addCInfoTab;

});
