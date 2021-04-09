$(document).ready(function () {
    $('#writer').addClass('active');
    $.ajax({
        url: '/writer/get-data-writer',
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


$('#form-add').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);

    $.ajax({
        url: '/writer/add-writer',
        method: 'POST',
        data: form.serialize(),
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
            alert('This writer already exists!');
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
        url: '/writer/get-data-writer',
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
<td>`+ aData.items[i].name + `</td>
<td>`+ aData.items[i].slug + `</td>
<td>`+ aData.items[i].biography + `</td>
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
            url: '/writer/delete',
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
        url: '/writer/get-detail-writer',
        method: 'POST',
        data: {
            'id': id
        },
        dataType: 'json',
        success: function (aData) {
            var sHtml = `
            <div class="form-group  required"><label class="form-control-label" for="editname">Name</label>
                <input class="form-control" id="editname" name="editname" required="" type="text" value="`+ aData.name + `">
            </div>
            <div class="form-group  required"><label class="form-control-label"
                    for="editbiography">Biography</label>
                <textarea class="form-control" id="editbiography" name="editbiography" required="" type="text"
                    cols="30" rows="10">`+ aData.biography + `</textarea>
            </div>
        `;
            $('#data-edit').html(sHtml);

            $('#save-change').click(function () {
                $.ajax({
                    url: '/writer/edit',
                    data: {
                        id: id,
                        name: $('#editname').val(),
                        biography: $('#editbiography').val()
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

$('#form-search').validate({
    showErrors: function (errorMap, errorList) {
        // Do nothing here
    },
    rules: {
        "search": {
            required: true
        }
    },
    submitHandler: function (form) {
        if ($('#search-name').val() == '') return;
        $.ajax({
            url: '/writer/search',
            method: 'POST',
            data: {
                'name': $('#search-name').val()
            },
            headers: {
                "Authorization": "Bearer " + getCookie('token'),
            },
            dataType: 'json',
            success: function (aData) {
                var sHtml = ``;
                for (i in aData.items) {
                    sHtml += `
                    <tr>
                    <td>`+ aData.items[i].id + `</td>
                    <td>`+ aData.items[i].name + `</td>
                    <td>`+ aData.items[i].slug + `</td>
                    <td>`+ aData.items[i].biography + `</td>
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
                $('#pagination').html('');
            },
            error: function () {
                location.reload();
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
});