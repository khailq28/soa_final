$(document).ready(function () {
    $('#sort').html(`
    <span>Sort by: </span>
    <select style="border: 1px solid #ced4da;" id="sort-by" name="sort-by">
        <option value="asc">Asc</option>
        <option value="desc">Desc</option>
    </select>
    `);


    $('#sort-by').change(function () {
        var sort_by = $(this).val();
        $.ajax({
            url: '/book/get-book-by-category',
            dataType: 'json',
            method: 'POST',
            data: {
                'page_num': 1,
                'order_by': sort_by,
                'category': $('#slug').val()
            },
            success: function (aData) {
                loadData(aData, sort_by);
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
    
    $.ajax({
        url: '/book/get-book-by-category',
        dataType: 'json',
        method: 'POST',
        data: {
            'page_num': 1,
            'order_by': 'asc',
            'category': $('#slug').val()
        },
        success: function (aData) {
            loadData(aData, "asc");
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

function change(page, orderBy) {
    $.ajax({
        url: '/book/get-book-by-category',
        dataType: 'json',
        method: 'POST',
        data: {
            'page_num': page,
            'order_by': orderBy,
            'category': $('#slug').val()
        },
        success: function (aData) {
            loadData(aData, orderBy);
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