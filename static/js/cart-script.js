console.log("Hello World")

function cart_detail_view($this){
	var productPk = $this.dataset.product
	var action = $this.dataset.action
	var pageId = $this.dataset.id

	console.log('productPk: ', productPk, 'Action:', action)
	console.log('USER: ', user)
	
	console.log('page: ', pageId)

	if (user == 'AnonymousUser'){
		LoginSignUpFunction(productPk)
		console.log("User is not logged in")
	}else{
		console.log("User is logged in")
		updateUserOrder(productPk, action, pageId)
	}	
}

function updateUserOrder(productPk, action, pageId){
	console.log('User is authenticated, sending data...')

	var url = '/ajax/cart/detail/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'Accept': 'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'productPk':productPk, 'action':action, 'pageId':pageId})
	})
	.then((response) => {
	   return response.json();
	})
	.then((data) => {
		var notif_tag = document.getElementById('AlreadyAdded'+productPk.toString());
	
		if(pageId == "cart-page")
			location.reload()
		console.log(data["done_action"])
		// {"added":False, "removed":False, "cleared":False, "new_added":False}
		if (notif_tag != null){
			if (data["added"] == true && pageId == "product-page"){
				// alert("New product added to your cart.")
				// notif_tag.innerHTML = 'Добавлено в корзину';
				notif_tag.classList.toggle("show");
				// added_to_cart()
			}
			if (data["already_added"] == true && pageId == "product-page"){
				// alert("This product was already added to your cart.")
				notif_tag.innerHTML = 'Уже выбрано';
				notif_tag.classList.toggle("show");
			}
		}
	});
}

// When the user clicks on div, open the popup
function LoginSignUpFunction(productPk) {
	console.log("This method works fine")
	var popup = document.getElementById("PopupNotification"+productPk.toString());
	popup.classList.toggle("show");
  }


// (function(){
// 	$('.add-to-basket').on('click', function(e){
// 	  e.preventDefault();
// 	  $.notify('Продукт был добавлен в корзину.', 'success','5000','top');
// 	});
  
//   })(jQuery);

// function added_to_cart(){
// 	// e.preventDefault();
// 	$.notify('Продукт был добавлен в корзину.', 'success','5000','top');
// }