
        $(document).ready(function () {
            if (getCookie('cart') != undefined) {
                var arr = JSON.parse(getCookie('cart')||null);
                if (arr.length == 0) location.replace('/');
            } else location.replace('/');

            var json_str = getCookie('cart');
            var arr = JSON.parse(json_str);
            for (i in arr) {
                $.ajax({
                    url: '/book/get-detail-book-cart',
                    dataType: 'json',
                    method: 'POST',
                    data: {
                        'id': arr[i].id,
                        'count': arr[i].count
                    },
                    success: function (aData) {
                        var sHtml = `
                        <tr class="cake-top" id="element`+ aData.id + `">
                            <td class="cakes">
                                <div class="product-img">
                                    <a href="/book/`+ aData.slug + `"><img src="../static/images/books/` + aData.image + `"  width="150" height="auto"></a>
                                </div>
                            </td>
                            <td class="cake-text">
                                <div class="product-text">
                                    <a href="/book/`+ aData.slug + `"><h1>` + aData.title + `</h1></a>
                                    <p>In stock: `+ aData.number + `</p>
                                </div>
                            </td>
                            <td class="quantity">
                                <div class="product-right">
                                    <input min="1" type="number" id="quantity" name="quantity`+ aData.id + `" value="` + aData.count + `"
                                        class="form-control input-small" pattern="/^-?\d+\.?\d*$/" onKeyPress="if (this.value.length == 10) return false;" onkeydown="javascript: return event.keyCode === 8 ||
                                                    event.keyCode === 46 ? true : !isNaN(Number(event.key))">
                                </div>
                            </td>
                            <td class="price">
                                <div style="display: flex;"><h4>$</h4><h4 id="price`+ aData.id + `">` + aData.price + `</h4></div>
                            </td>
                            <td class="top-remove">
                                <div style="display: flex;"><h4>$</h4><h4 id="total`+ aData.id + `">` + aData.total + `</h4></div>
                                <div class="close" id="`+ aData.id + `">
                                    <h5>Remove</h5>
                                </div>
                            </td>

                        </tr>
                        `;
                        $('#list').append(sHtml);


                        //event
                        $('#' + aData.id).click(function () {
                            $('#code').val('');
                            $('#element' + aData.id).fadeOut('slow', function () {
                                $('#element' + aData.id).remove();
                            });

                            //change cookie
                            var json_str = getCookie('cart');
                            var arr = JSON.parse(json_str);
                            for (i in arr) {
                                if (arr[i].id == aData.id) {
                                    arr.splice(i, 1);
                                    break;
                                }
                            }
                            var json_str = JSON.stringify(arr);
                            loadTotal(json_str, null);
                            document.cookie = "cart=" + json_str + '; path=/';
                        });

                        $('input[name="quantity' + aData.id + '"]').focusout(function () {
                            $('#code').val('');
                            if ($(this).val() == 0) $(this).val(1);

                            if ($(this).val() > aData.number) {
                                $(this).val(1);
                                alert('Not enough quantity');
                            }
                            //change cookie
                            var json_str = getCookie('cart');
                            var arr = JSON.parse(json_str);

                            for (i in arr) {
                                if (arr[i].id == aData.id) {
                                    arr[i].count = $(this).val();
                                    break;
                                }
                            }
                            var json_str = JSON.stringify(arr);
                            loadTotal(json_str, null);
                            document.cookie = "cart=" + json_str + '; path=/';

                            $('#total' + aData.id).html(parseInt($(this).val()) * parseInt($('#price' + aData.id).text()));
                        });
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
            loadTotal(JSON.stringify(arr), null);

            //check login
            $.ajax({
                url: '/check-login',
                dataType: 'json',
                method: 'POST',
                success: function (aData) {
                    if (aData.login) {
                        $.ajax({
                            url: '/get-info',
                            dataType: 'json',
                            method: 'GET',
                            headers: {
                                "Authorization": "Bearer " + getCookie('token'),
                            },
                            success: function (aData) {
                                var sHtml = `
                                <div class="row" style="margin-top: 5px; margin-bottom: 5px; display: flex;">
                                    <div style="width: 30%;">
                                        <b style="font-weight: bold;">Name:</b>
                                    </div>
                                    <div style="width: 70%;">
                                        <p>`+ aData.firstname + ` ` + aData.lastname + `</p>
                                    </div>
                                </div>
                                <div class="row" style="margin-top: 5px; margin-bottom: 5px; display: flex;">
                                    <div style="width: 30%;">
                                        <b style="font-weight: bold;">Email:</b>
                                    </div>
                                    <div style="width: 70%;">
                                        <p>`+ aData.email + `</p>
                                    </div>
                                </div>
                                <div class="row" style="margin-top: 5px; margin-bottom: 5px; display: flex;">
                                    <div style="width: 30%;">
                                        <b style="font-weight: bold;">Address:</b>
                                    </div>
                                    <div style="width: 70%;">
                                        <p>`+ aData.address + `</p>
                                    </div>
                                </div>
                                <div class="row" style="margin-top: 5px; margin-bottom: 5px; display: flex;">
                                    <div style="width: 30%;">
                                        <b style="font-weight: bold;">Phone number:</b>
                                    </div>
                                    <div style="width: 70%;">
                                        <p>`+ aData.phone + `</p>
                                    </div>
                                </div>
                                <div class="row" style="margin-top: 5px; margin-bottom: 5px; display: flex;">
                                    <div style="width: 30%;">
                                        <b style="font-weight: bold;">Payment method:</b>
                                    </div>
                                    <div style="width: 30%;">
                                        <select id="payment-method" class="form-control">
                                            <option value="cash">Cash</option>
                                            <option value="ibanking">IBanking</option>
                                        </select>
                                    </div>
                                </div>
                                `;
                                $('#info').html(sHtml);
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

        function loadTotal(arr_id, coupon) {
            var arr = JSON.parse(arr_id);
            if (arr.length == 0) location.replace('/');
            $.ajax({
                url: '/book/get-total-price',
                dataType: 'json',
                method: 'POST',
                data: {
                    'data': arr_id,
                    'coupon': coupon
                },
                success: function (aData) {
                    if (aData.message != null) {
                        alert(aData.message);
                    } else {
                        $('#total').text('Total: $' + aData.total);
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

        $('#form-coupon').submit(function (e) {
            e.preventDefault(); // avoid to execute the actual submit of the form.

            var form = $(this);
            var url = form.attr('action');

            if ($('#code').val() != '') {
                $.ajax({
                    url: '/coupon/check-coupon',
                    dataType: 'json',
                    method: 'POST',
                    data: form.serialize(),
                    success: function (aData) {
                        if (aData.message != null) {
                            alert(aData.message);
                        } else {
                            var json_str = getCookie('cart');
                            var arr = JSON.parse(json_str);
                            var json_str = JSON.stringify(arr);
                            loadTotal(json_str, $('#code').val());
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

        $('#payment').click(function () {
            //check login
            $.ajax({
                url: '/check-login',
                dataType: 'json',
                method: 'POST',
                success: function (aData) {
                    if (!aData.login) {
                        window.location.pathname = '/signin';
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

            var json_str = getCookie('cart');
            var arr = JSON.parse(json_str);
            var json_str = JSON.stringify(arr);

            var sMethod = $('#payment-method').val();
            var sDiscount = $('#code').val();
            if (sMethod != 'ibanking' && sMethod != 'cash') return;
            //order 
            $.ajax({
                url: '/order',
                dataType: 'json',
                data: {
                    'order': json_str,
                    'payment-method': sMethod,
                    'discount': sDiscount
                },
                method: 'POST',
                headers: {
                    "Authorization": "Bearer " + getCookie('token'),
                },
                success: function (aData) {
                    alert(aData.message);
                    document.cookie = "cart=; expires=Thu, 01 Jan 1970 00:00:00 UTC;"
                    window.location.pathname = '/';
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