$(document).ready(function () {
    $.ajax({
        url: '/get-info',
        dataType: 'json',
        method: 'GET',
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        success: function (aData) {
            $('#name').html(aData.firstname + ` ` + aData.lastname);
            $('#email').html(aData.email);
            $('#address').html(aData.address);
            $('#phone').html(aData.phone);
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
        url: '/order/get-detail-order',
        dataType: 'json',
        method: 'POST',
        data: {
            'id': $('#id').val()
        },
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        success: function (aData) {
            var list_book = JSON.parse(aData.order_info.order)
            for (i in list_book) {
                fGetDataBook(list_book[i].id, list_book[i].count);
            }
            $('#code').val(aData.order_info.coupon.code);
            $('#total').html('Total: $' + aData.order_info.total);
            $('#method').html(aData.method);
            $('#status').html(aData.status);
            $('#created').html(aData.created);
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
function fGetDataBook(id, count) {
    $.ajax({
        url: '/book/get-detail-book-cart',
        dataType: 'json',
        method: 'POST',
        data: {
            'id': id,
            'count': count
        },
        success: function (aData) {
            var sHtml = `
                <tr class="cake-top" id="element`+ aData.id + `">
                    <td class="cakes">
                        <div class="product-img">
                            <a href="/book/`+ aData.slug + `"><img src="../static/images/books/` + aData.image + `"  width="150" height="auto"></a>
                        </div>
                    </td>
                    <td class="cake-text">
                        <div class="product-text">
                            <a href="/book/`+ aData.slug + `"><h1>` + aData.title + `</h1></a>
                        </div>
                    </td>
                    <td class="quantity">
                        <div class="product-right">
                            <p>` + aData.count + `</p>
                        </div>
                    </td>
                    <td class="price">
                        <div style="display: flex;"><h4>$</h4><h4 id="price`+ aData.id + `">` + aData.price + `</h4></div>
                    </td>
                    <td class="top-remove">
                        <div style="display: flex;"><h4>$</h4><h4 id="total`+ aData.id + `">` + aData.total + `</h4></div>
                    </td>

                </tr>
                `;
            $('#list').append(sHtml);
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