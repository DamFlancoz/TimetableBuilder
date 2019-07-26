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
            this.lecture = "";
            this.lab = "";
            this.tutorial = "";
        }

        /**
         * Might be overridden to set the lecture section for course from input.
         */
        getLecture() {
            return this;
        }

        /**
         * Might be overridden to set the lab section for course from input.
         */
        getLab() {
            return this;
        }

        /**
         * Might be overridden to set the tutorial section for course from input.
         */
        getTutorial() {
            return this;
        }
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
    $tables = $("#tables");

    /**
     * @global
     * @type {jQuery Object} Saves tag which can contain the messages to user(errors).
     */
    $messages = $("#messages");
});
