


$('#recipeCarousel').carousel({
  interval: 1000
});

$('.carousel .carousel-item').each(function(){
    var minPerSlide = 3;
    var next = $(this).next();
    if (!next.length) {
    next = $(this).siblings(':first');
    }
    next.children(':first-child').clone().appendTo($(this));
    
    for (var i=0;i<minPerSlide;i++) {
        next=next.next();
        if (!next.length) {
          next = $(this).siblings(':first');
        }
        
        next.children(':first-child').clone().appendTo($(this));
      }
});



window.replainSettings = { id: 'e977c27a-cfa5-4635-be9d-c2db2f6ba9c2' };
(function(u){var s=document.createElement('script');s.type='text/javascript';s.async=true;s.src=u;
var x=document.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);
})('https://widget.replain.cc/dist/client.js');



  $(document).ready(function(){

    $.fakeLoader({
      timeToHide:1000,
      bgColor:"#ff780f",
      // spinner:"spinner1",
      //spinner:"spinner2",
      // spinner:"spinner3",
      // spinner:"spinner4",
      //spinner:"spinner5",
      //spinner:"spinner6",
      spinner:"spinner7",
      // imagePath:"../img/logo.png",
    });




  });
    


  function remove_or_add($this){
    var buttonId = $this.dataset.id;
    var productPk = $this.dataset.product;
    var order_quantity = 1
    if (buttonId == "add"){
      console.log("add", productPk)
      increase_quantity(productPk)
    } else {
      console.log("remove", productPk)
      decrease_quantity(productPk)
    }
  }

  function increase_quantity(pk){
    var input_value = document.getElementById('OrderQuantity'+pk.toString()).value;
    input_value++;
    document.getElementById('OrderQuantity'+pk.toString()).value = input_value;
  }
  function decrease_quantity(pk){
    var input_value = document.getElementById('OrderQuantity'+pk.toString()).value;
    input_value--;
    if (input_value <= 0) {
      return;
    }
    document.getElementById('OrderQuantity'+pk.toString()).value = input_value;
  }




  // $('.add-quantity-btn').click(function(){

  //   var productQuantityIpt = $(this).closest(".quantityBtnGroup").find(".quantity-input");
  //   var productQuantityInput = $(this).closest(".quantityBtnGroup").find(".quantity-input").value;

  //   var productQuantity = parseInt(productQuantityInput, 10); 
    
  //   productQuantity++;
  
  //   productQuantityIpt.value = productQuantity;
  //   });
  





$('.remove-quantity-btn').click(function(){
  var productQuantityIpt = $(this).closest(".quantityBtnGroup").find(".quantity-input");
  var productQuantityInput = $(this).closest(".quantityBtnGroup").find(".quantity-input").value;
  var productQuantity = parseInt(productQuantityInput, 10); 
  
  productQuantity--;
   
  if (productQuantity <= 0) {
    return;
  }
  
  productQuantityIpt.value = productQuantity;


});







  // Crol to top
  var $btnTop = $(".btn-top");
  $(window).on("scroll",function(){
    if($(window).scrollTop() >= 20)
    {
      $btnTop.fadeIn();
    }
    else{
      $btnTop.fadeOut();
    }
  });
  $btnTop.on("click",function(){
    $("html,body").animate({scrollTop:0},1200)
  });


  
 
