function pagination(current_page, pages, next_num, prev_num) {
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
            <a class="page-link" tabindex="-1" onclick="change(`+ prev_num +`)">Previous</a>
            </li>
        `;
    }

    if (pages <= 6) {
        for(i=1;i<=pages;i++) {
            if (i == current_page)
                sHtml += `
                <li class="page-item active">
                <a class="page-link">`+ i +` <span class="sr-only">(current)</span></a>
                </li>
                `;
            else
                sHtml += `
                <li class="page-item no"><a class="page-link" onclick="change(`+ i +`)">`+ i +`</a></li>
                `;
        }
    }
    else {
        var pageCutLow = current_page - 1;
        var pageCutHigh = current_page + 1;
        if (current_page > 2) {
            sHtml += `<li class="page-item"><a class="page-link" onclick="change(1)">1</a></li>`;
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
            sHtml += `<li class="page-item `+ active +`"><a class="page-link" onclick="change(`+p+`)">` + p + `</a></li>`;
        }

        if (current_page < pages - 1) {
            if (current_page < pages - 2) {
                sHtml += `<li class="page-item"><a class="page-link">...</a></li>`;
            }
            sHtml += `<li class="page-item"><a class="page-link" onclick="change(`+pages+`)">`+pages+`</a></li>`;
        }
    }

    if (next_num == null) {
            sHtml += `
            <li class="page-item disabled">
            <a class="page-link" onclick="change(`+ next_num +`)">Next</a>
            </li></ul>
            `;
        } else {
            sHtml += `
            <li class="page-item">
            <a class="page-link" tabindex="-1" onclick="change(`+ next_num +`)">Next</a>
            </li></ul>
            `;
        }
        $('#pagination').html(sHtml);
}