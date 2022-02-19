from django.shortcuts import render
from django.views import View
from .models import Comment,LikeComment
from django.contrib.auth.mixins import LoginRequiredMixin
from book.models import Book
from .forms import CommentForm

class CommentLikeView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        comment = Comment.objects.get(id=kwargs['comment_id'])
        book = Book.objects.get(id=kwargs['book_id'])
        like_comment =LikeComment.objects.filter(comment=comment,user=request.user)
        if not like_comment.exists():
            LikeComment.objects.create(comment=comment,user=request.user)

        comments = Comment.objects.filter(book=book)
        return render(request, 'book/detail.html', {'book': book, 'comments': comments, 'comment_form': CommentForm})

