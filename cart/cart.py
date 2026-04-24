from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if cart is None:
            cart = self.session['cart'] = {}
        self.cart = cart  # Ensure cart is assigned correctly

    def add(self, product, quantity=1):
        # Adds a product to the cart or updates its quantity.
        product_id = str(product.id)  # Store product ID as string
        if product_id in self.cart and isinstance(self.cart[product_id], dict):  # Ensure dict structure
            self.cart[product_id]['quantity'] += int(quantity)  # Update quantity
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': int(quantity)  # Store quantity as integer
            }

        self.session.modified = True  # Ensure session is updated

    def cart_total(self):
        """Calculates the total price of all items in the cart."""
        product_ids = self.cart.keys()  # To collect product ids
        products = Product.objects.filter(id__in=product_ids)  # Retrieve products from DB
        quantities = self.cart  # Collect quantities
        total = 0  # Initialize total to 0
        
        # Iterate over each item in the cart
        for key, value in quantities.items():
            key = int(key)  # Convert the string key to integer
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value['quantity'])  # Calculate total for this product
                    else:
                        total += (product.price * value['quantity']) 
                            

        return total

    def __len__(self):
        # Returns the total quantity of all items in the cart.
        return sum(int(item.get('quantity', 0)) for item in self.cart.values() if isinstance(item, dict))

    def get_prods(self):
        """Retrieve products from the database based on stored IDs."""
        product_ids = self.cart.keys()
        return Product.objects.filter(id__in=product_ids)

    def get_quants(self):
        """Returns the quantity of each product in the cart."""
        return {pid: item['quantity'] for pid, item in self.cart.items() if isinstance(item, dict)}

    def update(self, product, quantity):
        """Updates the quantity of a product in the cart."""
        product_id = str(product.id)  # Convert product ID to string
        product_qty = int(quantity)

        if product_id in self.cart and isinstance(self.cart[product_id], dict):
            self.cart[product_id]['quantity'] = product_qty  #  Ensures dictionary structure
        else:
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': product_qty
            }

        self.session.modified = True  # Required for session update
        return self.cart

    def delete(self, product):
        #Deletes a product from the cart
        product_id = str(product.id)  # Convert product ID to string
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True
