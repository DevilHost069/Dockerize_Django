$(".owl-carousel").owlCarousel({
    autoplay: true,
    loop: true,
    center: true,
    margin:5,
    animateOut: 'slideOutDown',
    animateIn: 'flipInX',
    nav:true,
    autoplayhoverpause: true,
    autoplaytimeout: 30,
    responsiveClass:true,
    responsive:{
        0:{
            items:2,
            nav:false
        },
        300:{
            items:2,
            nav:false
        },
        500:{
            items:2,
            nav:true
        },
        600:{
            items:3,
            nav:false
        },
        1000:{
            items:6,
            nav:true,
        }
    }

  });


  $("#id_category").change(function () {
    const url = $("#loaddataform").attr("data-subcategory-url");  // get the url of the `load_cities` view
    const categoryId = $(this).val();  // get the selected country ID from the HTML input
    console.log(categoryId)
    console.log(url)
    $.ajax({                       // initialize an AJAX request
        url: url,                    // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'category_id': categoryId       // add the country id to the GET parameters
        },
        success: function (data) {   // `data` is the return of the `load_cities` view function
            $("#id_subcategory").html(data);  // replace the contents of the city input with the data that came from the server
            // if (data.responseValue == 'MobilePhones'){
            //     $('.testhide').hide();
            // }
            // $(".displaynonefield").hide()
            // if (categoryId == 'ccceaa05-ffc0-469a-8431-b70f66bcd62e'){
            //     $("#pcshowhide").show()
            //     $("#pcshowhide1").show()
            // }
            // else if (categoryId == '69f6b484-17a3-4c49-8be5-96d8de05d7be'){
            //     $("#vechshowhide").show()
            //     $("#vechshowhide1").show()
            // }
            
            // let html_data = '<option value="">---------</option>';
            // data.forEach(function (subcategoryobj) {
            //     html_data += `<option value="${subcategoryobj.id}">${subcategoryobj.name}</option>`
            // });
            // console.log(html_data);
            // $("#id_subcategory").html(data);

            
        }
    });

});

$(function(){
    $(".btnClose").click(function(){
        $(".alertDivclose").alert('close');
    })
});

setTimeout(function () {
  
    // Closing the alert
    $('.alert').alert('close');
}, 2000);


$(document).on('click', '#delete-item', () => {
    document.getElementById("item-delete-form").action = document.querySelector('#delete-item').href
});
