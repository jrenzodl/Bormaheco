/**
 * Created by Ira Macazo on 11/07/2017.
 */

$(document).ready(function () {
    /** CSRF FOR AJAX **/

    function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    /** CSRF FOR AJAX **/

    $("#login").click(function()
    {
        var username = $("#login_username_input").val();
        var password = $("#login_password_input").val();
        $.ajax
        (
            {
                type: 'POST',
                url: '../login/',
                data:{
                    username: username,
                    password: password
                },
                success:[ function(data)
                {
                    if(data === "True")
                        window.location.reload();
                    else
                    {
                        $("#loginerror").fadeIn();
                        setTimeout(function() {
                          $("#loginerror").fadeOut();
                        }, 2000);
                    }
                }]
            }
        )
    })

});