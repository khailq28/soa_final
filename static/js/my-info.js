$(document).ready(function () {
    loadInfo();
});

$("#form-update").validate({
    onfocusout: false,
    onkeyup: false,
    onclick: false,
    debug: true,
    success: "valid",
    rules: {
        "lastname": {
            required: true,
            rangelength: [1, 15]
        },
        "firstname": {
            required: true,
            rangelength: [1, 15]
        },
        "email": {
            required: true,
        },
        "address": {
            required: true,
            maxlength: 100
        },
        "phone": {
            required: true,
            number: true,
            rangelength: [10, 10]
        },
    },
    submitHandler: function (form) {
        $.ajax({
            url: '/change-info',
            dataType: 'json',
            data: $('form').serialize(),
            method: 'POST',
            headers: {
                "Authorization": "Bearer " + getCookie('token'),
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
});

function loadInfo() {
    $.ajax({
        url: '/get-info',
        dataType: 'json',
        method: 'GET',
        headers: {
            "Authorization": "Bearer " + getCookie('token'),
        },
        success: function (aData) {
            console.log(aData);
            $('#firstname').val(aData.firstname);
            $('#lastname').val(aData.lastname);
            $('#username').val(aData.username);
            $('#money').val(aData.money);
            $('#address').val(aData.address);
            $('#phone').val(aData.phone);
            $('#email').val(aData.email);
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