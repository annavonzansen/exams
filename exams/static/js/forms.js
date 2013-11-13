function selectFirstField() {
    $('form:not(.filter) :input:visible:first').focus();
}

function fillEmptyAmount() {

}

$(document).ready(function() {
    selectFirstField();

    $("input.amount").focusout(function() {
        var val = $(this).val().trim();
        if (val == '') {
            $(this).val(0);
        }
    });
});