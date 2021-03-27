$("#reset").validate({
    onfocusout: false,
    onkeyup: false,
    onclick: false,
    debug: true,
    success: "valid",
    rules: {
        "password": {
            required: true,
            rangelength: [8, 15]
        },
        "confirm": {
            required: true,
            equalTo: "#password",
            rangelength: [8, 15]
        },
    },
    submitHandler: function (form) {
        $.ajax({
            url: '/change-password',
            dataType: 'json',
            data: $('form').serialize(),
            method: 'POST',
            success: function (aData) {
                var sHtml = `
                <form class="form" action="/signin">
                    <h3>`+ aData.message +`</h3>
                    <button class="form__button button" style="cursor: pointer;">Return sign in</button>
                </form>
                `;
                $('#content').html(sHtml);
            },
            error: function () {
                alert('error');
            },
            beforeSend: function () {
                $('selector').css('cursor', 'progress');
            },
            complete: function () {
                $('selector').css('cursor', 'pointer');
            }
        });
    }
});