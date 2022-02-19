from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages

from cart.cart import Cart
from .models import Order, OrderItem
from book.models import Book
from .tasks import send_email_task
from .pay import PayZarinpal


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        book_ids = cart.book_ids()
        if len(book_ids) > 0:
            order = Order.objects.create(user=request.user)
            for book_id in book_ids:
                book = Book.objects.get(id=book_id)
                OrderItem.objects.create(order=order, book=book)
            cart.clear()
            messages.info(request, 'your order is save', 'info')
            return redirect('order:detail', order.id)
        messages.warning(request, 'your cart is empty', 'warning')
        return redirect('home')


class DetailOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        return render(request, 'order/detail.html', {'order': order})


class StartPayView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        pay = PayZarinpal(request, amount=order.get_total_price())
        result_request = pay.ready_to_requeat("desc")
        if result_request[0]:
            order.authority_zarinpal = result_request[1]
            order.save()
            return pay.send_request(result_request[1])
        else:
            return HttpResponse(f"Error code")


class VerifyPayView(View):
    def get(self, request, *args, **kwargs):
        authority = self.request.GET['Authority']
        order = get_object_or_404(Order, authority_zarinpal=authority)
        pay = PayZarinpal(request, amount=order.get_total_price())
        result_verify = pay.verify(authority)
        if result_verify[0]:
            order.ref_if_zarinpal = result_verify[1]
            order.paid = True
            order.save()
            links = [item.link_download for item in order.items.all()]
            send_email_task.delay('BookHop',
                                  'links for download: ' + '\n'.join(links), request.user.email)
            return HttpResponse('Transaction success.\nRefID: ')
        else:
            return HttpResponse('Transaction failed or canceled by user')
