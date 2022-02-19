from django.urls import path
from . import views

app_name = 'order'


urlpatterns = [

    path('create/', views.CreateOrderView.as_view(), name='create'),
    path('request/<int:order_id>/', views.StartPayView.as_view(), name='request'),
    path('<int:order_id>/', views.DetailOrderView.as_view(), name='detail'),
    path('verify/', views.VerifyPayView.as_view(), name='verify'),

]
