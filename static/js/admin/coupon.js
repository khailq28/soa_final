$('#percent').focusout(function() {
    if ($(this).val() > 100)    $(this).val('');
});
$(document).ready(function () {
    $('#coupon').addClass('active');
    $.ajax({
        url: '/coupon/get-all-coupon',
        method: 'POST',
        dataType: 'json',
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        success: function (aData) {
            loadData(aData);
        },
        error: function () {
            alert('error');
        },
        beforeSend: function () {
            $('#loading').css('display', 'block');
        },
        complete: function () {
            $('#loading').css('display', 'none');
        }
    });
});


$('#form-add').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);

    $.ajax({
        url: '/coupon/add-coupon',
        data: form.serialize(),
        method: 'POST',
        dataType: 'json',
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        success: function (aData) {
            alert(aData.message);
            location.reload();
        },
        error: function () {
            location.reload();
            alert('This coupon already exists!');
        },
        beforeSend: function () {
            $('#loading').css('display', 'block');
        },
        complete: function () {
            $('#loading').css('display', 'none');
        }
    });
});

function loadData(aData) {
    var sHtml = ``;
    for (i in aData.items) {
        sHtml += `
<tr>
<td>`+ aData.items[i].code + `</td>
<td>`+ aData.items[i].percent * 100 + `%</td>
<td>`+ aData.items[i].description + `</td>
<td>`+ aData.items[i].time_start + `</td>
<td>`+ aData.items[i].time_end + `</td>
<td>`+ aData.items[i].created + `</td>
<td>
<div class="row" style="margin: auto">
    <i class="fa fa-trash btn btn-danger btn-delete" style="margin-bottom: 1%" aria-hidden="true" onclick="deleteWriter('`+ aData.items[i].code + `')"></i>
</div>
</td>
</tr>
`;
    }
    $('#data').html(sHtml);
}

function deleteWriter(code) {
    var r = confirm("Are you sure you want to delete it?");
    if (r == true) {
        $.ajax({
            url: '/coupon/delete',
            method: 'DELETE',
            dataType: 'json',
            headers: {
                "Authorization": "Bearer " + getCookie('token'),
            },
            data: {
                'code': code
            },
            success: function (aData) {
                alert(aData.message);
                location.reload();
            },
            error: function () {
                alert('error');
            },
            beforeSend: function () {
                $('#loading').css('display', 'block');
            },
            complete: function () {
                $('#loading').css('display', 'none');
            }
        });
    }
}