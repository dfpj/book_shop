from django.shortcuts import render,redirect
from .cart import Cart
from book.models import Book
from django.contrib import messages

def show_carts(request):
    cart = Cart(request)
    book_ids = cart.book_ids()
    books =[]
    total_price = 0
    if len(book_ids) > 0 :
        for id in book_ids:
            book = Book.objects.get(id=id)
            books.append(book)
            total_price += book.price
        return render(request, 'cart/show_carts.html',{'books':books,'total_price':total_price})
    messages.warning(request,'your cart is empty','warning')
    return redirect('book:home')
def add_cart(request,book_id):
    cart = Cart(request)
    cart.add(book_id)
    return redirect('cart:show_carts')