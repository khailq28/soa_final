$("#a-form").validate({
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
        "username": {
            required: true,
            rangelength: [8, 15]
        },
        "email": {
            required: true,
        },
        "password": {
            required: true,
            rangelength: [8, 15]
        },
        "confirm": {
            required: true,
            equalTo: "#password",
            rangelength: [8, 15]
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
        if (confirm('Your text here')) {
            // user clicked on Yes
        }
        else {
            // user clicked on No
        }
        $.ajax({
            url: '/signup',
            dataType: 'json',
            data: $('form').serialize(),
            method: 'POST',
            success: function (aData) {
                alert(aData.message);
            },
            error: function () {
                alert('Account already exists');
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
$("#b-form").validate({
    onfocusout: false,
    onkeyup: false,
    onclick: false,
    debug: true,
    success: "valid",
    rules: {
        "i-username": {
            required: true,
            rangelength: [8, 15]
        },
        "i-password": {
            required: true,
            rangelength: [8, 15]
        },
    },
    submitHandler: function (form) {
        $.ajax({
            url: '/signin',
            dataType: 'json',
            data: $('form').serialize(),
            method: 'POST',
            success: function (aData) {
                console.log(aData);
                if (aData.login) {
                    document.cookie = "token=" + aData.token;
                    window.location.replace('\home');
                } else {
                    alert(aData.message);
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
});