$('#logout').click(function () {
    $.ajax({
        url: '/logout',
        method: 'POST',
        dataType: 'json',
        success: function (aData) {
            if (aData.logout) {
                location.reload();
            }
        },
        beforeSend: function () {
            $('#loading').css('display', 'block');
            document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC;"
        },
        complete: function () {
            $('#loading').css('display', 'none');
        }
    });
});