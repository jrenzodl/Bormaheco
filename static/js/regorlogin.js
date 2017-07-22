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

        if(location !== "" && startdate !== "" && enddate !== "")
        {
            $("#registermodal").modal();
        }
    });

    var createuser = function(){
        var username = $("#register_username").val();
        var password1 = $("#register_password").val();
        var email = $("#register_email").val();
        var company = $("#register_company").val();
        var location = $("#location").val();
        var startdate = $("#datestart").val();
        var enddate = $("#dateend").val();
        var comments = document.getElementById("remarks").value;

        $.ajax({
            type: 'POST',
            url: register_url,
            data:{
                username: username,
                password: password1,
                email: email,
                company: company,
                location: location,
                startdate: startdate,
                enddate: enddate,
                comments: comments
            },
            success: function(){
                    window.location.href = transaction;
                    return false;
            }
        })
    };

    $("#register").click(function () {
       var username = $("#register_username").val();
       var password1 = $("#register_password").val();
       var password2 = $("#register_password2").val();
       var email = $("#register_email").val();
       var company = $("#register_company").val();

       var validemail = true;
       var validpassword = true;

       $('#reg_user_group').attr("class", 'form-group text-left');
       $('#reg_username_error').attr('hidden', true);

       $('#reg_password_group').attr("class", 'form-group text-left');
       $('#reg_password_error').attr('hidden', true);

       $('#reg_password2_group').attr("class", 'form-group text-left');
       $('#reg_password2_error').attr('hidden', true);

       $('#reg_email_group').attr("class", 'form-group text-left');
       $('#reg_email_error').attr('hidden', true);

       $('#reg_company_group').attr("class", 'form-group text-left');
       $('#reg_company_error').attr('hidden', true);

       if(username === "")
       {
           $('#reg_user_group').attr("class", 'form-group text-left has-error');
           $('#reg_username_error').html("Please input username").removeAttr('hidden');
       }

       if(password1 === "")
       {
           $('#reg_password_group').attr("class", 'form-group text-left has-error');
           $('#reg_password_error').html("Please input password").removeAttr('hidden');
       }

       if(password2 === "")
       {
           $('#reg_password2_group').attr("class", 'form-group text-left has-error');
           $('#reg_password2_error').html("Please confirm password").removeAttr('hidden');
       }

       if(email === "")
       {
           $('#reg_email_group').attr("class", 'form-group text-left has-error');
           $('#reg_email_error').html("Please input email").removeAttr('hidden');
       }
       else if( !(/(.+)@(.+){2,}\.(.+){2,}/.test(email)))
       {
           $('#reg_email_group').attr("class", 'form-group text-left has-error');
           $('#reg_email_error').html("Please input valid email").removeAttr('hidden');
           validemail = false;
       }

       if(company === "")
       {
           $('#reg_company_group').attr("class", 'form-group text-left has-error');
           $('#reg_company_error').html("Please input company").removeAttr('hidden');
       }

       if(password1 !== password2)
       {
            $('#reg_password_group').attr("class", 'form-group text-left has-error');
            $('#reg_password2_group').attr("class", 'form-group text-left has-error');
            $('#reg_password2_error').html("Passwords do not match").removeAttr('hidden');
            validpassword = false;
       }

        if(username !== "" && password1 !== "" && password2 !== "" && email !== "" && validemail === true &&
            company !== "" && validpassword === true)
        {
            $.ajax({
                type: 'POST',
                url: check_user_url,
                data: {
                    username: username
                },
                success: function (data) {
                    if(data === "yes")
                    {
                        $('#reg_user_group').attr("class", 'form-group text-left has-error');
                        $('#reg_username_error').html("Username is taken").removeAttr('hidden');
                    }
                    else
                        createuser();
                }
            });
        }
    });

    $("#login2").click(function() {
        var username = $("#username_login").val();
        var password = $("#password_login").val();
        var location = $("#location").val();
        var startdate = $("#datestart").val();
        var enddate = $("#dateend").val();
        var comments = document.getElementById("remarks").value;

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
                        password: password,
                        location: location,
                        startdate: startdate,
                        enddate: enddate,
                        comments: comments
                    },
                    success:[ function(data)
                    {
                        if(data === "True")
                        {
                            window.location.href = transaction;
                            return false;
                        }
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

    $("#loggedincheckout").click(function () {
        var location = $("#location").val();
        var startdate = $("#datestart").val();
        var enddate = $("#dateend").val();
        var comments = document.getElementById("remarks").value;

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

        if(location !== "" && startdate !== "" && enddate !== "")
        {
            $.ajax({
                type: 'POST',
                url: checkout,
                data:{
                    location: location,
                    comments: comments,
                    startdate: startdate,
                    enddate: enddate
                },
                success: function(){
                    window.location.href = transaction;
                    return false;
                }
            })
        }
    });
});