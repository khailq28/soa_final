$(document).ready(function () {
    $('#order').addClass('active');
    $.ajax({
        url: '/order/get-all-order',
        data: {
            'page_num': 1
        },
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        method: 'POST',
        dataType: 'json',
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

function change(page) {
    $('#pagination').html('');
    $.ajax({
        url: '/order/get-all-order',
        data: {
            'page_num': page
        },
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        method: 'POST',
        dataType: 'json',
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
}

function loadData(aData) {
    var sHtml = ``;
    for (i in aData.items) {
        sHtml += `
<tr>
<td>`+ aData.items[i].id + `</td>
<td>`+ aData.items[i].created + `</td>
<td>$`+ aData.items[i].total_price + `</td>
<td>`+ aData.items[i].status + `</td>
<td>`+ aData.items[i].firstname + ` `+ aData.items[i].lastname + `</td>
<td>`+ aData.items[i].email + `</td>
<td>`+ aData.items[i].address + `</td>
<td>`+ aData.items[i].phone_number + `</td>
<td>
<div class="row" style="margin: auto">
<i class="far fa-trash-alt btn btn-danger btn-delete" style="margin-bottom: 1%" aria-hidden="true" onclick="deleteWriter('`+ aData.items[i].id + `')"></i>
<a href='/admin/detail/`+ aData.items[i].id + `'><i class="fas fa-info btn btn-warning"></i><a/>
</div>
</td>
</tr>
`;
    }
    $('#data').html(sHtml);
    pagination(aData.current_page, aData.pages, aData.next_num, aData.prev_num);
}

function deleteWriter(id) {
    var r = confirm("Are you sure you want to delete it?");
    if (r == true) {
        $.ajax({
            url: '/order/delete',
            method: 'DELETE',
            data: {
                'id': id
            },
            headers: {
                "Authorization": "Bearer " + getCookie('token'),
            },
            dataType: 'json',
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
