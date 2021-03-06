$(document).ready(function () {
    if (getCookie('cart') != undefined) {
        var arr = JSON.parse(getCookie('cart')||null);
        if (arr.length == 0) $('#num-product').html('0');
        else    $('#num-product').html(arr.length);
    } else $('#num-product').html('0');
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