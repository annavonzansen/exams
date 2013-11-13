function selectFirstField() {
    $('form:not(.filter) :input:visible:first').focus();
}

$(document).ready(function() {
    selectFirstField();
});