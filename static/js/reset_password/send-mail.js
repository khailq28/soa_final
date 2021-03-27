$("#forgot").validate({
    onfocusout: false,
    onkeyup: false,
    onclick: false,
    debug: true,
    success: "valid",
    rules: {
        "email": {
            required: true,
        },
    },
    submitHandler: function (form) {
        $.ajax({
            url: '/forgot',
            dataType: 'json',
            data: $('form').serialize(),
            method: 'POST',
            success: function (aData) {
                var sHtml = `
                <form class="form" action="/signin">
                    <h2 class="form_title title">Reset password</h2>
                    <h3>`+ aData.message + `</h3>
                    <button class="form__button button" style="cursor: pointer;">Return sign in</button>
                </form>
                `;
                $('#content').html(sHtml);
            },
            error: function () {
                alert('error');
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