$(document).ready(function () {
    $.ajax({
        url: '/book/get-detail-book',
        dataType: 'json',
        method: 'POST',
        data: {
            'id': $('#id').val()
        },
        success: function (aData) {
            var sWriter = '';
            if (aData.writer.length > 1) {
                for (j in aData.writer) {
                    if (j == aData.writer.length - 1)
                        sWriter += `<a href="/writer/` + aData.writer[j].slug + `">` + aData.writer[j].name + `</a>`;
                    else
                        sWriter += `<a href="/writer/` + aData.writer[j].slug + `">` + aData.writer[j].name + `</a>` + `, `;
                }
            } else {
                sWriter = `<a href="/writer/` + aData.writer[0].slug + `">` + aData.writer[0].name + `</a>`;
            }
            $('#image').html(`<img src="../static/images/books/` + aData.image + `" height="auto" width="250" alt="">`);
            $('#title').html(aData.title);
            $('#writers').html(sWriter + ` (Author)`);
            $('.price').html(`$` + aData.price);
            $('#price-detail').html(`$` + aData.price);
            $('#description').html(aData.info);
            $('#publisher').html(aData.publisher);
            $('#publish-date').html(aData.publish_date);
            $('#pages').html(aData.pages);
            $('#type').html(aData.category);
            $('#quantity').html(aData.number);
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
    loadComment();
});

$("#form-comment").validate({
    onfocusout: false,
    onkeyup: false,
    onclick: false,
    debug: true,
    success: "valid",
    showErrors: function (errorMap, errorList) {
        // Do nothing here
    },
    rules: {
        "content": {
            required: true,
        },
    },
    submitHandler: function (form) {
        $.ajax({
            url: '/comment',
            dataType: 'json',
            data: $('form').serialize(),
            method: 'POST',
            headers: {
                "Authorization": "Bearer " + getCookie('token'),
            },
            success: function (aData) {
                alert(aData.message);
                $('#content').val('');
                loadComment();
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

function loadComment() {
    $.ajax({
        url: '/get-comment',
        dataType: 'json',
        method: 'POST',
        data: {
            'id': $('#id').val()
        },
        success: function (aData) {
            if (aData.comments.length > 0) {
                var sHtml = ``;
                for (i in aData.comments) {
                    sHtml += `
                    <div class="comment-element">
                        <div class="comment-box">
                            <div class="comment-head">
                                <h6 class="comment-name by-author">`+ aData.comments[i].firstname + ` ` + aData.comments[i].lastname + `</h6>
                                <span>`+ aData.comments[i].created + `</span>
                            </div>
                        </div>
                        <div class="comment-content">
                            `+ aData.comments[i].content + `
                        </div>
                    </div>
                    `;
                }
                $('#list-comment').html(sHtml);
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
}

$('#add-cart').click(function () {
    if (getCookie('cart') == null) {
        var arr = [];
        arr.push({ 'id': $('#id').val(), 'count': 1 });
    } else {
        var json_str = getCookie('cart');
        var arr = JSON.parse(json_str);
        var bCheck = true;
        for (i in arr) {
            if (arr[i].id == $('#id').val()) {
                arr[i].count++;
                bCheck = false;
                break;
            }
        }
        if (bCheck) arr.push({ 'id': $('#id').val(), 'count': 1 });
    }
    var json_str = JSON.stringify(arr);
    document.cookie = "cart=" + json_str + '; path=/';
    json_str = getCookie('cart');
    var arr = JSON.parse(json_str);
    $('#num-product').html(arr.length);
    alert('Add successful!');
});