(function () {
    var input = document.getElementById("id_image"),
        formdata = false;
      
    function showUploadedItem (source) {
        var img  = document.getElementById("preview");
        img.src = source;
        img.className = "thumbnail";
    }

    if (input.addEventListener) {
        input.addEventListener("change", function (evt) {
            var i = 0, len = this.files.length, img, reader, file;
                file = this.files[i];
            if (!!file.type.match(/image.*/)) {
                if ( window.FileReader ) {
                    reader = new FileReader();
                    reader.onloadend = function (e) {
                        showUploadedItem(e.target.result);
                    };
                    reader.readAsDataURL(file);
                }
            }
        }, false);
    }

    $("form#data").submit(function() {
        var formdata = new FormData();
            csrf_token = $("input[name=csrfmiddlewaretoken]").val();
            input_string = $("#id_note").val();
            input_image = $("#id_image");
            file = input_image[0].files[0];
            // file = this.files[0];
        formdata.append('csrfmiddlewaretoken', csrf_token);
        formdata.append('note', input_string);
        formdata.append("image", file);
        $.ajax({
            url: "/ajaxnotes_json",
            type: "POST",
            dataType: 'json',
            data: formdata,
            processData: false,
            contentType: false,
            success : function(json) {
                if (json.new_note){
                    $('#notes_list').prepend( json.new_note );
                    $("#id_note").val("");
                    $("#count").text(json.count);
                    $("#message").text(json.message);
                    $("#errors-note ul li").html("");
                    $("#errors-image ul li").html("");
                    $("#id_note").css("border-color", "rgb(204, 204, 204)");
                }
                else {
                    $("#errors-note ul li").html( json.error_note );
                    $("#errors-image ul li").html( json.error_image );
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
})();