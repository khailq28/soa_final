$(document).ready(function () {
    $('#category').addClass('active');
    $.ajax({
        url: '/category/get-all-categories',
        method: 'POST',
        dataType: 'json',
        success: function (aData) {
            for (i in aData.category) {
                var sHtml = `
                <tr>
                    <td>`+ aData.category[i].name + `</td>
                    <td>`+ aData.category[i].slug + `</td>
                    <td>`+ aData.category[i].created + `</td>
                    <td>
                        <button type="button" class="btn btn-danger btn-delete" 
                        onclick="deleteCategory('`+ aData.category[i].name + `')">Delete</button>
                    </td>
                </tr>
                `;
                $('#data').append(sHtml);
            }
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
        url: '/category/add-category',
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
            alert('This category already exists!');
        },
        beforeSend: function () {
            $('#loading').css('display', 'block');
        },
        complete: function () {
            $('#loading').css('display', 'none');
        }
    });
});


function deleteCategory(name) {
    var r = confirm("Are you sure you want to delete it?");
    if (r == true) {
        $.ajax({
            url: '/category/delete',
            method: 'DELETE',
            data: {
                'name' : name
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