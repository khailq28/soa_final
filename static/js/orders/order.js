$.ajax({
    url: '/order/get-orders',
    dataType: 'json',
    method: 'POST',
    headers: {
        "Authorization": "Bearer " + getCookie('token'),
    },
    success: function (aData) {
        // var sHtml = ``;
        for (i in aData.data) {
            var sHtml = `
            <div class="element" id="`+ aData.data[i].id + `">
                <div class="row">
                    <div id="ele-id">ID: <span id="data">`+ aData.data[i].id + `</span></div>
                    <div id="ele-date">Order date: <span id="data">`+ aData.data[i].created + `</span></div>
                    <div id="ele-status">`+ aData.data[i].status + `</div>
                </div>
                <div class="row">
                    <div id="ele-total">Total price: <span id="price">$`+ aData.data[i].total_price + `</span></div>
                </div>
            </div>
            `;
            $('#list-book').append(sHtml);
            fShowDetail(aData.data[i].id);
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

function fShowDetail(id) {
    $('#' + id).click(function () {
        window.location = '/detail/'+id;
    });
}