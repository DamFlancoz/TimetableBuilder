/**
 * @fileoverview Contains all functions to help event listeners' definitions.
 */

/**
 * Checks if the course inputted by user is already selected.
 * @nosideeffects @global
 */
export function courseAlreadySelected() {

    return selectedCourses.reduce((acc, curr) => {
        return acc || ($cName.val() === curr.name && $cNum.val() === curr.num);
    }, false);
}
