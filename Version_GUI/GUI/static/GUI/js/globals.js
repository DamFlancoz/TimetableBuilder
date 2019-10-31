$(function () {
    /**
     * @fileoverview Cashes frequently used objects:
     *  - Defines global variables for saving information.
     *  - Cashes frequently accessed elements.
     *  - Course class.
     */

    /**
     * @class Course is used to save selected courses to pass for building table. getLecture
     * or any methods are overwritten to get user input once back-end returns ajax
     * request success fully.
     *
     * @global
     */
    class Course {

        /**
         * @param {string} name Name of course to select.
         * @param {string} num Number of course to select.
         */
        constructor(name, num) {
            this.name = name;
            this.num = num;
            this.$panel = "";
        }

        /**
         * Might be overridden to set the lecture section for course from input.
         */
        getLecture() {
            return this.$panel.find("[name=lecture]:checked").val() || "";
        }

        /**
         * Might be overridden to set the lab section for course from input.
         */
        getLab() {
            return this.$panel.find("[name=lab]:checked").val() || "";
        }

        /**
         * Might be overridden to set the tutorial section for course from input.
         */
        getTutorial() {
            return this.$panel.find("[name=tutorial]:checked").val() || "";
        }
    }

    Course.prototype.toString = function () {
        return `${this.name} ${this.num}`;
    }

    window.Course = Course;

    // Globals
    /**
     * @global
     * @type {Array<Course>} Saves selected courses.
     */
    selectedCourses = [];

    /**
     * @global
     * @type {jQuery Object} Saves term input field. Used to get inputted term.
     */
    $term = $("#term");

    /**
     * @global
     * @type {jQuery Object} Saves name input field. Used to get inputted course name.
     */
    $cName = $("#cName");

    /**
     * @global
     * @type {jQuery Object} Saves no. input field. Used to get inputted course no.
     */
    $cNum = $("#cNum");


    //Cashing course-info window and tables window
    /**
     * @global
     * @type {jQuery Object} Saves tag which contains all course tabs.
     */
    $cInfo = $("#cInfo");

    /**
     * @global
     * @type {jQuery Object} Saves tag which contains the timetable displayed.
     */
    $table = $("#table");

    /**
     * @global
     * @type {jQuery Object} Saves tag which can contain the messages to user(errors).
     */
    $messages = $("#messages");
});
