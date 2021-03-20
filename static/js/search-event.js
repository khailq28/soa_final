$('#form-search').validate({
    showErrors: function (errorMap, errorList) {
        // Do nothing here
    },
    rules: {
        "search": {
            required: true
        }
    },
    submitHandler: function (form) {
        $('#sort').html('');
        $('#info').html('');
        $('#products').html('');
        var value = $('#search').val();
        var search_by = $('#search_by').val();
        $.ajax({
            url: '/book/search',
            dataType: 'json',
            method: 'POST',
            data: {
                'page_num': 1,
                'value': value,
                'search_by': search_by
            },
            success: function (aData) {
                var orderBy = "asc";
                loadDataSearch(aData, value, search_by);
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

function loadDataSearch(aData, value, search_by) {
    var sHtml = ``;
    for (i in aData.items) {
        var sWriter = '';
        if (aData.items[i].writer.length > 1) {
            for (j in aData.items[i].writer) {
                if (j == aData.items[i].writer.length - 1)
                    sWriter += `<a href="/writer/` + aData.items[i].writer[j].slug + `">` + aData.items[i].writer[j].name + `</a>`;
                else
                    sWriter += `<a href="/writer/` + aData.items[i].writer[j].slug + `">` + aData.items[i].writer[j].name + `</a>` + `, `;
            }
        } else {
            sWriter = `<a href="/writer/` + aData.items[i].writer[0].slug + `">` + aData.items[i].writer[0].name + `</a>`;
        }
        sHtml += `
            <div class="col-md-4">
                <div class="book-card">
                    <div class="book-card__cover">
                        <div class="book-card__book">
                            <div class="book-card__book-front">
                                <a href="/book/`+ aData.items[i].slug + `">
                                    <img class="book-card__img" src="../static/images/books/` + aData.items[i].image + `" /></a>
                            </div>
                            <div class="book-card__book-back"></div>
                            <div class="book-card__book-side"></div>
                        </div>
                    </div>
                    <div>
                        <div class="book-card__title">
                            <a href="/book/`+ aData.items[i].slug + `" id='title-book'>
                                ` + aData.items[i].title + `</a>
                        </div>
                        <div class="book-card__author">
                            `+ sWriter + `
                        </div>
                        <div class="price">
                            $`+ aData.items[i].price + `
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    $('#products').html(sHtml);
    paginationSearch(aData.current_page, aData.pages, aData.next_num, aData.prev_num, value, search_by);
}

function changeSearch(page, value, search_by) {
    $.ajax({
        url: '/book/search',
        dataType: 'json',
        method: 'POST',
        data: {
            'page_num': page,
            'value': value,
            'search_by': search_by
        },
        success: function (aData) {
            loadDataSearch(aData, value, search_by);
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

function paginationSearch(current_page, pages, next_num, prev_num, value, search_by) {
    if (prev_num == null) {
        var sHtml = `
<ul class="pagination">
<li class="page-item disabled">
<a class="page-link" tabindex="-1">Previous</a>
</li>
`;
    } else {
        var sHtml = `
<ul class="pagination">
<li class="page-item">
<a class="page-link" tabindex="-1" onclick="changeSearch(`+ prev_num + `, '` + value + `', '` + search_by + `')">Previous</a>
</li>
`;
    }

    if (pages <= 6) {
        for (i = 1; i <= pages; i++) {
            if (i == current_page)
                sHtml += `
<li class="page-item active">
<a class="page-link">`+ i + ` <span class="sr-only">(current)</span></a>
</li>
`;
            else
                sHtml += `
<li class="page-item no"><a class="page-link" onclick="changeSearch(`+ i + `, '` + value + `', '` + search_by + `')">` + i + `</a></li>
`;
        }
    }
    else {
        var pageCutLow = current_page - 1;
        var pageCutHigh = current_page + 1;
        if (current_page > 2) {
            sHtml += `<li class="page-item"><a class="page-link" onclick="changeSearch(1, '` + value + `', '` + search_by + `')">1</a></li>`;
            if (current_page > 3)
                sHtml += `<li class="page-item"><a class="page-link">...</a></li>`;
        }
        // Determine how many pages to show after the current page index
        if (current_page === 1) {
            pageCutHigh += 2;
        } else if (current_page === 2) {
            pageCutHigh += 1;
        }
        // Determine how many pages to show before the current page index
        if (current_page === pages) {
            pageCutLow -= 2;
        } else if (current_page === pages - 1) {
            pageCutLow -= 1;
        }
        // Output the indexes for pages that fall inside the range of pageCutLow and pageCutHigh
        for (var p = pageCutLow; p <= pageCutHigh; p++) {
            if (p === 0) {
                p += 1;
            }
            if (p > pages) {
                continue
            }
            var active = (current_page == p) ? "active" : "no"
            sHtml += `<li class="page-item ` + active + `"><a class="page-link" onclick="changeSearch(` + p + `, '` + value + `', '` + search_by + `')">` + p + `</a></li>`;
        }

        if (current_page < pages - 1) {
            if (current_page < pages - 2) {
                sHtml += `<li class="page-item"><a class="page-link">...</a></li>`;
            }
            sHtml += `<li class="page-item"><a class="page-link" onclick="changeSearch(` + pages + `, '` + value + `', '` + search_by + `')">` + pages + `</a></li>`;
        }
    }

    if (next_num == null) {
        sHtml += `
<li class="page-item disabled">
<a class="page-link" onclick="changeSearch(`+ next_num + `, '` + value + `', '` + search_by + `')">Next</a>
</li></ul>
`;
    } else {
        sHtml += `
<li class="page-item">
<a class="page-link" tabindex="-1" onclick="changeSearch(`+ next_num + `, '` + value + `', '` + search_by + `')">Next</a>
</li></ul>
`;
    }
    $('#pagination').html(sHtml);
}