/**
 * Created by Ira Macazo on 21/07/2017.
 */

$(document).ready(function () {

    $("#modalbutton").click(function(){

        var location = $("#location").val();
        var startdate = $("#datestart").val();
        var enddate = $("#dateend").val();

        $('#location_group').attr("class", 'form-group');
        $('#location_error').html("Please input a location").attr('hidden', true);

        $('#date_group').attr("class", 'form-group');
        $('#date_error').html("Please input a location").attr('hidden', true);

        if(location === "")
        {
            $('#location_group').attr("class", 'form-group has-error');
            $('#location_error').html("Please input a location").removeAttr('hidden');
        }
        if(startdate === "" || enddate === "")
        {
            $('#date_group').attr("class", 'form-group has-error');
            $('#date_error').html("Please input a proper date range").removeAttr('hidden');
        }

        if(location !== "")
        {
            $("#registermodal").modal();
        }
    });

    $("#login2").click(function() {
        var username = $("#username_login").val();
        var password = $("#password_login").val();

        $('#login_username_group').attr("class", 'form-group text-left');
        $('#login_username_error').html("Please input username").attr('hidden', true);

        $('#login_password_group').attr("class", 'form-group text-left');
        $('#login_password_error').html("Please input password").attr('hidden', true);

        if(username === "")
        {
            $('#login_username_group').attr("class", 'form-group text-left has-error');
            $('#login_username_error').html("Please input username").removeAttr('hidden');
        }

        if(password === "")
        {
            $('#login_password_group').attr("class", 'form-group text-left has-error');
            $('#login_password_error').html("Please input password").removeAttr('hidden');
        }


        if(username !=="" && password !=="")
        {
            $.ajax
            (
                {
                    type: 'POST',
                    url: login_checkout_url,
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
                            $('#login_username_group').attr("class", 'form-group text-left has-error');
                            $('#login_password_group').attr("class", 'form-group text-left has-error');
                            $('#login_password_error').html("Username and Password do not match").removeAttr('hidden');
                        }
                    }]
                }
            )
        }
    });
});