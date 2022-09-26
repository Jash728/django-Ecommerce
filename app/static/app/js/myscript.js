$('#slider1, #slider2, #slider3').owlCarousel({
    loop: false,
    rewind: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: false,
            autoplay: true,
            rewind: true,
        }
    }
})

$('.plus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var el = this.parentNode.children[2];
    // console.log(id);
    $.ajax({
        type: "GET",
        url: "/pluscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            el.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount

        }
    })
})

$('.minus-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var el = this.parentNode.children[2];
    // console.log(id);
    $.ajax({
        type: "GET",
        url: "/minuscart",
        data: {
            prod_id: id
        },
        success: function(data) {
            el.innerText = data.quantity
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount

        }
    })
})

$('.remove-cart').click(function() {
    var id = $(this).attr("pid").toString();
    var el = this;
    // console.log(id);
    $.ajax({
        type: "GET",
        url: "/removecart",
        data: {
            prod_id: id
        },
        success: function(data) {
            document.getElementById('amount').innerText = data.amount
            document.getElementById('totalamount').innerText = data.totalamount
            el.parentNode.parentNode.parentNode.parentNode.remove()

        }
    })
})