from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        #get request
        self.request = request
        #get the current session key if it exists
        cart = self.session.get('session_key')

        #if the user is new, no session key! then create one.
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        #make sure cart is available on all pages of site
        self.cart = cart 


    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        #checking if the product is added to the cart
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # converting {'3':1, '2':4} to {"3":1, "2":4} basically meaning converting python dictionary to string
            carty =  str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the profile model
            current_user.update(old_cart=str(carty))


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        #checking if the product is added to the cart
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # converting {'3':1, '2':4} to {"3":1, "2":4} basically meaning converting python dictionary to string
            carty =  str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the profile model
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        #get product ids
        product_ids = self.cart.keys()
        #lookup those keys in our product database model
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        #start counting from 0
        total = 0
        for key, value in quantities.items():
            #convert key string into int 
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                      total = total + (product.sale_price * value)
                    else:
                         total = total + (product.price * value)
        return total

    
    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #get ids from cart
        product_ids = self.cart.keys()
        #use ids to lookup products in database model
        products = Product.objects.filter(id__in=product_ids)
        #return those looked up products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities    
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        ourcart = self.cart
        # update dictionart/cart
        ourcart[product_id] = product_qty
        
        self.session.modified = True

        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # converting {'3':1, '2':4} to {"3":1, "2":4} basically meaning converting python dictionary to string
            carty =  str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the profile model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing
    
    def delete(self, product):
        product_id = str(product)
        #delete from dictionart/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True
        #deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # converting {'3':1, '2':4} to {"3":1, "2":4} basically meaning converting python dictionary to string
            carty =  str(self.cart)
            carty = carty.replace("\'", "\"")
            #save carty to the profile model
            current_user.update(old_cart=str(carty))
