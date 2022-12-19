
$(document).ready(function () {
    $(selector).click(function () { 
        $.ajax({
            type: "method",
            url: "url",
            data: "data",
            dataType: "dataType",
            success: function (response) {
                
            }
        });
    });
});
