from django.urls import path
from . import views


app_name = 'cart'

urlpatterns = [
    path('',views.show_carts,name='show_carts'),
    path('add/<int:book_id>/',views.add_cart,name='add_cart'),
]