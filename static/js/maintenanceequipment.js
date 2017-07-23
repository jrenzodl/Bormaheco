/**
 * Created by Ira Macazo on 23/07/2017.
 */

$(document).ready(function(){
    $(".submitcost").click(function(){
        var id = $(this).parent().parent().parent().attr("id");
        var cost = $("#cost_input" + id).val();

        $("#cost_group" + id).attr('class', "form-group text-left");
        $('#cost_error' + id).html("Please input cost").attr('hidden', true);

        if(cost === ''){
            $("#cost_group" + id).attr('class', "form-group text-left has-error");
            $('#cost_error' + id).html("Please input cost").removeAttr('hidden');
        }
        else{
            $.ajax({
                type: "POST",
                url: endmaintenance,
                data: {
                    cost: cost,
                    id: id
                },
                success: function () {
                    window.location.href = samepage;
                    return false;
                }

            });
        }
    });
});