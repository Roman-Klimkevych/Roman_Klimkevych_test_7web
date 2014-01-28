$(document).ready(function() {
    $("#add_note").click(function() {
        var input_string = $("#id_note").val();
        csrf_token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            url : "/ajaxnotes_json",
            type : "POST",
            dataType: "json",
            data : {
                note : input_string,
                csrfmiddlewaretoken: csrf_token
            },
            success : function(json) {
                if (json.new_note){
                    $('#notes_list').prepend( json.new_note );
                    $("#id_note").val("");
                    $("#count").text(json.count);
                    $("#message").text(json.message);
                    $("#errors ul li").html("");
                    $("#id_note").css("border-color", "rgb(204, 204, 204)");
                }
                else {
                    $("#errors ul li").html( json.errors );
                    $("#id_note").css("border-color", "red");
                    $("#message").text("");
                }
            },
            error : function(xhr,errmsg,err) {
                alert(xhr.status + ": " + xhr.responseText);
            }
        });
        return false;
    });
});