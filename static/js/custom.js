function sendArticleComment(articleId) {
    var comment = $("#commentText").val();
    var parentId = $('#parent_id').val();

    $.get('/articles/add_article_comment', {
        article_comment: comment,
        article_id: articleId,
        parent_id: parentId

    }).then(res => {
        console.log(res);
        $('#comments_area').html(res);
        $('#commentText').val('');
        $('#parent_id').val('');
        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: 'smooth'});
        } else {
            document.getElementById('comments_area').scrollIntoView({behavior: 'smooth'});

        }
    });
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: 'smooth'});
}

function sendProductComment(productId) {
    var comment = $('#text_area').val();
    console.log(comment);

    $.get('/products/add_product_comment/', {
        product_comment: comment,
        product_id: productId
    })
    document.location.reload()
}

function filterProducts() {
    const filterPrice = $('#sl2').val();
    const start_price = filterPrice.split(',')[0];
    const end_price = filterPrice.split(',')[1];
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#filter_form').submit();
}

function fillPage(page) {
    $('#page').val(page);
    $('#filter_form').submit();
}

function showLargeImage(imageSrc) {
    $('#main_image').attr('src', imageSrc);
    $('#show_large_image_modal').attr('href', imageSrc);
}

function addProductToOrder(productId) {
    const productCount = $('#product_count').val();
    $.get('/order/add_to_order?product_id=' + productId + '&count=' + productCount).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/login';
            }
        })
    });
}

function removeOrderDetail(detailId) {
    $.get('/user/remove_order_detail?detail_id=' + detailId).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: 'محصول با موقیت از سبد خرید حذف شد',
            icon: 'success',
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'باشه ممنون'
        })

        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    })
}

// state => decrease or increase
function changeOrderDetailCount(detailId, state) {
    $.get('/user/change_order_detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body);
        }
    })
}