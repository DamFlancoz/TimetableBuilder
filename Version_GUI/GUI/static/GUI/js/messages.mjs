
/**
 * @fileoverview Defines functions to handle messages to be given to user. Currently
 *  contains error posting and deleting methods.
 */

/**
 * Closure for methods dealing with error posting or messages for user.
 */

/**
 * Posts the given error to alert user.
 * @param {string} error The error to post to user.
 * @global
 */
export function postError(error) {

    /** @type {jQuery object} Holds error message. */
    let $message = $("<li>").addClass(`alert alert-danger ${error}`);

    switch (error) {
        case "already-in":
            $message.text("Course already selected");
            break;

        case "invalid-num":
            $message.text("'No.' is invalid");
            break;

        case "num-not-given":
            $message.text("'No.' not given");
            break;

        case "connection-error":
            $message.text("Error Ocurred in connecting to back-end");

        case "courses-not-fit":
            $message.text("Sections don't fit together");
    }

    // Post it to user
    $messages.append($message);
}

/**
 * Removes all errors posted to user.
 * @global
 */
export function removeErrors() {
    $messages.find(".alert-danger").remove();
}
