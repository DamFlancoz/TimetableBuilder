$(function () {
    //post error message
    window.postError = error => {
        // create message, marked with error (class alreadyIn)
        var $message = $("<li>").addClass(`alert alert-danger ${error}`);

        switch (error) {
            case "alreadyIn":
                $message.text("Course already selected");
                break;

            case "invalidNum":
                $message.text("'No.' is invalid");
                break;

            case "numNotGiven":
                $message.text("'No.' not given");
                break;

            case "connection-error":
                $message.text("Error Ocurred in connecting to back-end");
        }

        //Post it to user
        $messages.append($message);
    }

    //removes error messages to user
    window.removeErrors = () => {
        $(".alreadyIn").remove();
        $(".invalidNum").remove();
        $(".numNotGiven").remove();
        $(".connection-error").remove();
    }
});
