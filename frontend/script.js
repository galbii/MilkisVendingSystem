
let catalog = document.getElementById("catalog");

let cart = JSON.parse(localStorage.getItem("data")) || [];
let cartTotal = JSON.parse(localStorage.getItem("total")) || [];




let createCatalog = () => {
	return catalog.innerHTML = catalogItemsData.map((x)=>{
		let {id, item_name, price, quantity} = x 
		console.log(id);
		let locate = cart.find((x) => x.id === id) || []
		return `
		<div class="item">
			<img class = "left" src="temp.png" alt="temp" width="100">
			<div class="item">
		    	<h4>Item Name: <span id="itemName">${item_name}</span></h2>
		    	<p>Price: $<span id="itemPrice">${price}</span></p>
		    	<p>Stock: <span id="itemStock">${quantity}</span></p>
			</div>
			<div class="number-input">
		    	<button onclick="this.parentNode.querySelector('input[type=number]').stepDown(); decr(${id});" class="minus" id='minus'></button>
		    	<input id="counter" class="quantity" min="0" max ="${quantity}" value = "${locate.item === undefined ? 0: locate.item}" name="quantity" type="number" readonly="readonly"></input>
		    	<button onclick="this.parentNode.querySelector('input[type=number]').stepUp(); incr(${id});" class="plus" id = 'plus'></button>
			</div>
		</div>`;	
	}); 
};

createCatalog();
// Get the cart element and the plus button
const cartElement = document.getElementById('cart-value');
const plusButton = document.querySelectorAll('.plus');
const minusButton = document.querySelectorAll('.minus');
// Set the initial value
let cartValue = 0;
cartElement.textContent = cartValue;

// Add click event listener to the plus button
plusButton.forEach(function(plus){
	plus.addEventListener('click', function () {
    // Increment the cart value and update the display
    cartValue += 1;
});
});

minusButton.forEach(function(minus){
	minus.addEventListener('click', function () {
    // Increment the cart value and update the display
	if(cartValue != 0){
		cartValue -= 1;
	}
});
});	

let incr = (id) => {
    let chosenItem = id;
    let locate = cart.find((x)=> x.id === chosenItem)
	let located = catalogItemsData.find((y) => y.id === chosenItem) || [];
    if(locate === undefined){
        cart.push({
            id: chosenItem,
            item: 1,
        });
    }
	else if(locate.item === located.quantity) {
		cartValue -=1;
		cartElement.textContent = cartValue;
	}
    else{
        locate.item +=1;
    }
    
	let temporary = cartTotal.find((z)=> z.id === 0);
	if(temporary === undefined){
        cartTotal.push({
            id: 0,
            total: 1,
        });
    }
    else{
        temporary.total +=1;
    }
	localStorage.setItem("total", JSON.stringify(cartTotal));
	localStorage.setItem("data", JSON.stringify(cart));
	update();
};

let decr = (id) =>{
    let chosenItem = id;
    
    let locate = cart.find((x)=> x.id === chosenItem)
    if(locate === 0){
        return;
    }
    else{
        locate.item -=1;
    }

	let temporary = cartTotal.find((z)=> z.id === 0);
	if(temporary === 0){
        return;
    }
    else{
        temporary.total -=1;
    }
	localStorage.setItem("total", JSON.stringify(cartTotal));
	localStorage.setItem("data", JSON.stringify(cart));
    update();
};

let update = () => {
	let locate = cartTotal.find((x)=> x.id === 0);
	let total = locate.total;
	cartElement.textContent = total;
}

update();