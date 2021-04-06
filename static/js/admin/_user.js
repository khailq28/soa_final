$("#money").blur(function () {
    this.value = parseFloat(this.value).toFixed(2);
});
$(document).ready(function () {
    $('#user').addClass('active');
    $.ajax({
        url: '/get-all-user',
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
        url: '/get-all-user',
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
<td>`+ aData.items[i].username + `</td>
<td>`+ aData.items[i].email + `</td>
<td>`+ aData.items[i].firstname + `</td>
<td>`+ aData.items[i].lastname + `</td>
<td>`+ aData.items[i].address + `</td>
<td>`+ aData.items[i].phone_number + `</td>
<td>`+ aData.items[i].group + `</td>
<td>`+ aData.items[i].money + `</td>
<td>`+ aData.items[i].created + `</td>
<td>`+ aData.items[i].modified + `</td>
<td>
<div class="row" style="margin: auto">
    <i class="far fa-trash-alt btn btn-danger btn-delete" style="margin-bottom: 1%" aria-hidden="true" onclick="deleteWriter('`+ aData.items[i].id + `')"></i>
    <i class="fas fa-pen btn btn-warning" aria-hidden="true" onclick="editWriter('`+ aData.items[i].id + `')" data-toggle="modal" data-target="#modal"></i>
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
            url: '/delete',
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

function editWriter(id) {
    $.ajax({
        url: '/get-info-by-id',
        method: 'POST',
        data: {
            'id': id
        },
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        dataType: 'json',
        success: function (aData) {
            $('#group-id').val(aData.group);
            $('#email').val(aData.email);
            $('#firstname').val(aData.firstname);
            $('#lastname').val(aData.lastname);
            $('#address').val(aData.address);
            $('#phone').val(aData.phone_number);
            $('#money').val(aData.money);

            $('#save-change').click(function () {
                $.ajax({
                    url: '/edit',
                    data: {
                        'id' : id,
                        'group': $('#group-id').val(),
                        'email': $('#email').val(),
                        'firstname': $('#firstname').val(),
                        'lastname': $('#lastname').val(),
                        'address': $('#address').val(),
                        'phone': $('#phone').val(),
                        'money': $('#money').val(),
                    },
                    headers: {
                        "Authorization": "Bearer " + getCookie('token'),
                    },
                    dataType: 'json',
                    method: 'POST',
                    success: function (oData) {
                        alert(oData.message);
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
            });
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
