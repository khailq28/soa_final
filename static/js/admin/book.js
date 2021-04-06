$("#price").blur(function () {
    this.value = parseFloat(this.value).toFixed(2);
});
$("#price-edit").blur(function () {
    this.value = parseFloat(this.value).toFixed(2);
});
$(document).ready(function () {
    $('#book').addClass('active');
    $.ajax({
        url: '/book/get-all-book',
        dataType: 'json',
        method: 'POST',
        data: {
            'page_num': 1,
            'order_by': 'asc'
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

$('#writer-name').select2();
$('#writer-name-edit').select2();

$('#add').click(function () {
    $.ajax({
        url: '/book/get-data-form',
        dataType: 'json',
        method: 'POST',
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        success: function (aData) {
            sCategory = ``;
            for (i in aData.category) {
                sCategory += `<option value="` + aData.category[i].slug + `">` + aData.category[i].name + `</option>`;
            }
            $('#category-name').html(sCategory);

            sWriter = ``;
            for (i in aData.writer) {
                sWriter += `<option value="` + aData.writer[i].slug + `">` + aData.writer[i].name + `</option>`;
            }
            $('#writer-name').html(sWriter);
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

$('#form-save').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    $('#writers').val($('#writer-name').val());
    var form = new FormData();
    form.append("writers", $('#writers').val());
    form.append("category-name", $('#category-name').val());
    form.append("title", $('#title').val());
    form.append("info", $('#info').val());
    form.append("price", $('#price').val());
    form.append("publisher", $('#publisher').val());
    form.append("publish_date", $('#publish_date').val());
    form.append("pages", $('#pages').val());
    form.append("number", $('#number').val());
    form.append("image", $('#image')[0].files[0]);

    $.ajax({
        url: '/book/add-book',
        method: 'POST',
        data: form,
        dataType: 'json',
        processData: false,
        contentType: false,
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

function loadData(aData) {
    $('#data').html('');
    for (i in aData.items) {
        var sWriter = '';
        if (aData.items[i].writer.length > 1) {
            for (j in aData.items[i].writer) {
                if (j == aData.items[i].writer.length - 1)
                    sWriter += aData.items[i].writer[j].name;
                else
                    sWriter += aData.items[i].writer[j].name + ', ';
            }
        } else {
            sWriter = aData.items[i].writer[0].name;
        }
        var sHtml = `
        <tr>
            <td>`+ aData.items[i].id + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].category + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].title + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + sWriter + `</td>
            <td>`+ aData.items[i].slug + `</td>
            <td><img src="../static/images/books/`+ aData.items[i].image + `" alt="" style="width: 100px; height: 150px;">  <i class="fas fa-edit edit-image` + aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg3"></i></td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].info + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].price + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].publisher + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].publish_date + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].pages + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].number + `</td>
            <td>`+ aData.items[i].created + `</td>
            <td>`+ aData.items[i].modified + `</td>
            <td>
                <div class="row" style="margin: auto">
                    <i class="fa fa-trash btn btn-danger btn-delete" style="margin-bottom: 1%" aria-hidden="true" onclick="deleteWriter('`+ aData.items[i].id + `')"></i>
                </div>
            </td>
        </tr>
        `;
        $('#data').append(sHtml);
        fEditEvent(aData.items[i].id);
    }
    pagination(aData.current_page, aData.pages, aData.next_num, aData.prev_num);
}

function change(page) {
    $('#pagination').html('');
    $.ajax({
        url: '/book/get-all-book',
        dataType: 'json',
        method: 'POST',
        data: {
            'page_num': page,
            'order_by': 'asc'
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
}

function deleteWriter(id) {
    var r = confirm("Are you sure you want to delete it?");
    if (r == true) {
        $.ajax({
            url: '/book/delete',
            method: 'DELETE',
            dataType: 'json',
            headers: {
                "Authorization": "Bearer " + getCookie('token'),
            },
            data: {
                'id': id
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
        var value = $('#search').val();
        $.ajax({
            url: '/book/search-admin',
            dataType: 'json',
            method: 'POST',
            data: {
                'page_num': 1,
                'value': value,
            },
            headers: {
                "Authorization": "Bearer " + getCookie('token'),
            },
            success: function (aData) {
                loadDataSearch(aData, value);
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
});

function loadDataSearch(aData, value) {
    $('#data').html('');
    for (i in aData.items) {
        var sWriter = '';
        if (aData.items[i].writer.length > 1) {
            for (j in aData.items[i].writer) {
                if (j == aData.items[i].writer.length - 1)
                    sWriter += aData.items[i].writer[j].name;
                else
                    sWriter += aData.items[i].writer[j].name + ', ';
            }
        } else {
            sWriter = aData.items[i].writer[0].name;
        }
        var sHtml = `
        <tr>
            <td>`+ aData.items[i].id + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].category + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].title + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + sWriter + `</td>
            <td>`+ aData.items[i].slug + `</td>
            <td><img src="../static/images/books/`+ aData.items[i].image + `" alt="" style="width: 100px; height: 150px;">  <i class="fas fa-edit edit-image` + aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg3"></i></td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].info + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].price + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].publisher + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].publish_date + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].pages + `</td>
            <td><i class="fas fa-edit edit`+ aData.items[i].id + `" data-toggle="modal" data-target=".bd-example-modal-lg2"></i><br>` + aData.items[i].number + `</td>
            <td>`+ aData.items[i].created + `</td>
            <td>`+ aData.items[i].modified + `</td>
            <td>
                <div class="row" style="margin: auto">
                    <i class="fa fa-trash btn btn-danger btn-delete" style="margin-bottom: 1%" aria-hidden="true" onclick="deleteWriter('`+ aData.items[i].id + `')"></i>
                </div>
            </td>
        </tr>
        `;
        $('#data').append(sHtml);
        fEditEvent(aData.items[i].id);
    }
    paginationSearch(aData.current_page, aData.pages, aData.next_num, aData.prev_num, value);
}

function changeSearch(page, value) {
    $.ajax({
        url: '/book/search-admin',
        dataType: 'json',
        method: 'POST',
        data: {
            'page_num': page,
            'value': value,
        },
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        success: function (aData) {
            loadDataSearch(aData, value);
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

function paginationSearch(current_page, pages, next_num, prev_num, value) {
    if (prev_num == null) {
        var sHtml = `
<ul class="pagination">
<li class="page-item disabled">
<a class="page-link" tabindex="-1">Previous</a>
</li>
`;
    } else {
        var sHtml = `
<ul class="pagination">
<li class="page-item">
<a class="page-link" tabindex="-1" onclick="changeSearch(`+ prev_num + `, '` + value + `')">Previous</a>
</li>
`;
    }

    if (pages <= 6) {
        for (i = 1; i <= pages; i++) {
            if (i == current_page)
                sHtml += `
<li class="page-item active">
<a class="page-link">`+ i + ` <span class="sr-only">(current)</span></a>
</li>
`;
            else
                sHtml += `
<li class="page-item no"><a class="page-link" onclick="changeSearch(`+ i + `, '` + value + `')">` + i + `</a></li>
`;
        }
    }
    else {
        var pageCutLow = current_page - 1;
        var pageCutHigh = current_page + 1;
        if (current_page > 2) {
            sHtml += `<li class="page-item"><a class="page-link" onclick="changeSearch(1, '` + value + `')">1</a></li>`;
            if (current_page > 3)
                sHtml += `<li class="page-item"><a class="page-link">...</a></li>`;
        }
        // Determine how many pages to show after the current page index
        if (current_page === 1) {
            pageCutHigh += 2;
        } else if (current_page === 2) {
            pageCutHigh += 1;
        }
        // Determine how many pages to show before the current page index
        if (current_page === pages) {
            pageCutLow -= 2;
        } else if (current_page === pages - 1) {
            pageCutLow -= 1;
        }
        // Output the indexes for pages that fall inside the range of pageCutLow and pageCutHigh
        for (var p = pageCutLow; p <= pageCutHigh; p++) {
            if (p === 0) {
                p += 1;
            }
            if (p > pages) {
                continue
            }
            var active = (current_page == p) ? "active" : "no"
            sHtml += `<li class="page-item ` + active + `"><a class="page-link" onclick="changeSearch(` + p + `, '` + value + `')">` + p + `</a></li>`;
        }

        if (current_page < pages - 1) {
            if (current_page < pages - 2) {
                sHtml += `<li class="page-item"><a class="page-link">...</a></li>`;
            }
            sHtml += `<li class="page-item"><a class="page-link" onclick="changeSearch(` + pages + `, '` + value + `')">` + pages + `</a></li>`;
        }
    }

    if (next_num == null) {
        sHtml += `
<li class="page-item disabled">
<a class="page-link" onclick="changeSearch(`+ next_num + `, '` + value + `')">Next</a>
</li></ul>
`;
    } else {
        sHtml += `
<li class="page-item">
<a class="page-link" tabindex="-1" onclick="changeSearch(`+ next_num + `, '` + value + `')">Next</a>
</li></ul>
`;
    }
    $('#pagination').html(sHtml);
}

function fEditEvent(id) {
    $('.edit-image' + id).click(function() {
        $.ajax({
            url: '/book/get-detail-book',
            dataType: 'json',
            method: 'POST',
            data: {
                'id': id
            },
            success: function (aData) {
                $('#id-image').val(aData.id);
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
    $('.edit' + id).click(function () {
        $.ajax({
            url: '/book/get-data-form',
            dataType: 'json',
            method: 'POST',
            headers: {
                "Authorization": "Bearer " + getCookie('token'),
            },
            success: function (aData) {
                sCategory = ``;
                for (i in aData.category) {
                    sCategory += `<option value="` + aData.category[i].slug + `">` + aData.category[i].name + `</option>`;
                }
                $('#category-name-edit').html(sCategory);

                sWriter = ``;
                for (i in aData.writer) {
                    sWriter += `<option value="` + aData.writer[i].slug + `">` + aData.writer[i].name + `</option>`;
                }
                $('#writer-name-edit').html(sWriter);
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

        $.ajax({
            url: '/book/get-detail-book',
            dataType: 'json',
            method: 'POST',
            data: {
                'id': id
            },
            success: function (aData) {
                $('#category-name-edit').val(aData.slug_category);
                $('#title-edit').val(aData.title);
                $('#info-edit').val(aData.info);
                $('#price-edit').val(aData.price);
                $('#publisher-edit').val(aData.publisher);
                $('#publish_date-edit').val(aData.publish_date);
                $('#pages-edit').val(aData.pages);
                $('#number-edit').val(aData.number);
                $('#title-edit').val(aData.title);
                $('#id-edit').val(aData.id);
                var aWriter = [];
                if (aData.writer.length > 1) {
                    for (j in aData.writer) {
                        aWriter.push(aData.writer[j].slug);
                    }
                } else {
                    aWriter.push(aData.writer[0].slug);
                }
                $('#writer-name-edit').val(aWriter)
                $('#writer-name-edit').select2(aWriter);
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
}

$('#form-edit').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    $('#writers-edit').val($('#writer-name-edit').val());
    var form = new FormData();
    form.append("writers", $('#writers-edit').val());
    form.append("category-name", $('#category-name-edit').val());
    form.append("info", $('#info-edit').val());
    form.append("price", $('#price-edit').val());
    form.append("publisher", $('#publisher-edit').val());
    form.append("publish_date", $('#publish_date-edit').val());
    form.append("pages", $('#pages-edit').val());
    form.append("number", $('#number-edit').val());
    form.append("id", $('#id-edit').val());

    $.ajax({
        url: '/book/edit-book',
        method: 'POST',
        data: form,
        dataType: 'json',
        processData: false,
        contentType: false,
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

$('#form-edit-image').submit(function (e) {
    e.preventDefault(); // avoid to execute the actual submit of the form.
    var form = new FormData();
    form.append("id", $('#id-image').val());
    form.append("image", $('#image-edit')[0].files[0]);

    $.ajax({
        url: '/book/edit-image',
        method: 'POST',
        data: form,
        dataType: 'json',
        processData: false,
        contentType: false,
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