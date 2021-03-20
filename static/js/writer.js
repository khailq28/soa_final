$(document).ready(function () {
    $.ajax({
        url: '/writer/get-detail-writer',
        dataType: 'json',
        method: 'POST',
        data: {
            'id': $('#id').val()
        },
        success: function (aData) {
            $('#author').html(aData.name);
            $('#description').html(aData.biography);
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
        url: '/book/get-book-by-author',
        dataType: 'json',
        method: 'POST',
        data: {
            'page_num': 1,
            'writer_id': $('#id').val()
        },
        success: function (aData) {
            loadData(aData, $('#id').val());
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
function loadData(aData, id) {
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
    pagination(aData.current_page, aData.pages, aData.next_num, aData.prev_num, id);
}


function pagination(current_page, pages, next_num, prev_num, id) {
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
            <a class="page-link" tabindex="-1" onclick="change(`+ prev_num + `, '` + id + `')">Previous</a>
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
    <li class="page-item no"><a class="page-link" onclick="change(`+ i + `, '` + id + `')">` + i + `</a></li>
    `;
        }
    }
    else {
        var pageCutLow = current_page - 1;
        var pageCutHigh = current_page + 1;
        if (current_page > 2) {
            sHtml += `<li class="page-item"><a class="page-link" onclick="change(1, '` + id + `')">1</a></li>`;
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
            sHtml += `<li class="page-item ` + active + `"><a class="page-link" onclick="change(` + p + `, '` + id + `')">` + p + `</a></li>`;
        }

        if (current_page < pages - 1) {
            if (current_page < pages - 2) {
                sHtml += `<li class="page-item"><a class="page-link">...</a></li>`;
            }
            sHtml += `<li class="page-item"><a class="page-link" onclick="change(` + pages + `, '` + id + `')">` + pages + `</a></li>`;
        }
    }

    if (next_num == null) {
        sHtml += `
<li class="page-item disabled">
<a class="page-link" onclick="change(`+ next_num + `, '` + id + `')">Next</a>
</li></ul>
`;
    } else {
        sHtml += `
<li class="page-item">
<a class="page-link" tabindex="-1" onclick="change(`+ next_num + `, '` + id + `')">Next</a>
</li></ul>
`;
    }
    $('#pagination').html(sHtml);
}

function change(page, id) {
    $.ajax({
        url: '/book/get-book-by-author',
        dataType: 'json',
        method: 'POST',
        data: {
            'page_num': page,
            'writer_id': id
        },
        success: function (aData) {
            loadData(aData, id);
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