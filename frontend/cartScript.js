
let cart = JSON.parse(localStorage.getItem("data")) || [];
let cartTotal = JSON.parse(localStorage.getItem("total")) || [];

let ShopCart = document.getElementById("ShopCart");
let label = document.getElementById("label");

let generateCartItems = () => {
    if (cart.length !== 0) {
      return (ShopCart.innerHTML = cart
        .map((x) => {
          let { id, item } = x;
          let locate = catalogItemsData.find((y) => y.id === id) || [];
          return `
        <div class="item">
          <img width="100" src="temp.png" alt="" />
          <div class="details">
  
            <div class="itemcard">
                <h4 class="price">
                  <p>${locate.item_name}</p>
                  <p class="cart-item-price">$ ${locate.price}</p>
                </h4>
                <i onclick="removeItem(${id})" class="bi bi-x-lg"></i>
            </div>
  
            <div class="number-input">
		    	<input id="counter" class="quantity" min="0" max ="${locate.stock}" value = "${item}" name="quantity" type="number" readonly="readonly"></input>
			</div>
  
            <h3 class = "total-cost">$ ${item * locate.price}</h3>
          </div>
        </div>
        `;
        })
        .join(""));
    } else {
      ShopCart.innerHTML = ``;
      label.innerHTML = `
      <h2>Cart is Empty</h2>
      <a href="index.html">
        <button class="HomeBtn">Back to home</button>
      </a>
      `;
    }
  };

  let TotalAmount = () => {
    if (cart.length !== 0) {
      let amount = cart
        .map((x) => {
          let { item, id } = x;
          let search = catalogItemsData.find((y) => y.id === id) || [];
  
          return item * search.price;
        })
        .reduce((x, y) => x + y, 0);
      // console.log(amount);
      label.innerHTML = `
      <h2>Total Bill : $ ${amount}</h2>
      <button class="checkout">Checkout</button>
      <button onclick="clearCart()" class="removeAll">Clear Cart</button>
      `;
    } else return;
  };

let clearCart = () =>{
  cart = [];
  cartTotal = [];
  generateCartItems();
  localStorage.setItem("data", JSON.stringify(cart));
  localStorage.setItem("total", JSON.stringify(cartTotal));
};
  
generateCartItems();
TotalAmount();