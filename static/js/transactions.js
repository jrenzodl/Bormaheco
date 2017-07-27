$(document).ready(function () {
    $('#sendquotation').click(function () {
        var checkboxes = $('.check').length;
        var cost = $("#cost").val();
        var id = $("#detailsid").text();
        var equipmentforquotation = [];
        var comments = document.getElementById("remarks").value;
        for(var x = 0; x < checkboxes; x++)
        {
            if($('#eq' + x).is(':checked'))
            {
                equipmentforquotation.push($('#eq' + x).val())
            }
            else if($('#eq' + x).is(':disabled'))
            {
                if($('#replace' + x).val() !== "x" )
                    equipmentforquotation.push($('#replace' + x).val())
            }
        }

        $('#cost_group').attr("class", 'form-group');
        $('#cost_error').html("Please input a location").attr('hidden', true);

        if(cost === "")
        {
            $('#cost_group').attr("class", 'form-group has-error');
            $('#cost_error').html("Please input transportation cost").removeAttr('hidden');
        }
        else
        {
            $.ajax({
                type: "POST",
                url: createquotation,
                data:{
                    inquiryid: id,
                    'listofequipment[]': equipmentforquotation,
                    comments: comments,
                    cost: cost
                },
                success: function () {
                    window.location.href = transaction;
                    return false;
                }
            })
        }
    })
});