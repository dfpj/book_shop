CART_SESSION_NAME = 'dfpj_cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_NAME)
        if not cart:
            cart = self.session[CART_SESSION_NAME] = {}
        self.cart = cart

    def add(self, book_id):
        if str(book_id) not in self.cart:
            self.cart[str(book_id)] = {'id':str(book_id)}
        self.save()

    def book_ids(self):
        return self.cart.keys()


    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session[CART_SESSION_NAME]
        self.save()