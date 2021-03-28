$(document).ready(function () {
    var json_str = getCookie('cart');
    var arr = JSON.parse(json_str);
    $('#num-product').html(arr.length);
    //load category tabs
    $.ajax({
        url: '/category/get-all-categories',
        dataType: 'json',
        method: 'POST',
        success: function (aData) {
            var sHtml = ``;
            for (i in aData.category) {
                sHtml += `
                <li><a href="/category/`+ aData.category[i].slug + `">` + aData.category[i].name + `</a></li>
            `;
            }
            $('#category-tabs').html(sHtml);
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
    //load writer tabs
    $.ajax({
        url: '/writer/get-random-writer',
        dataType: 'json',
        method: 'POST',
        success: function (aData) {
            var sHtml = ``;
            for (i in aData.writer) {
                sHtml += `
                <li><a href="/writer/`+ aData.writer[i].slug + `">` + aData.writer[i].name + `</a></li>
            `;
            }
            $('#author-tabs').html(sHtml);
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