from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('like/<int:book_id><int:comment_id>/', views.CommentLikeView.as_view(), name='like'),

]
