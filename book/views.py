from django.core.paginator import Paginator
from django.http import HttpResponse
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import Book
from .forms import SearchBookForm
from order.models import OrderItem
from comments.models import Comment
from comments.forms import CommentForm


class DownloadFileView(View):
    def get(self, request, *args, **kwargs):
        item = get_object_or_404(OrderItem, link_download=settings.DEFAULT_DOMAIN + "download" + "/" + kwargs['token_link'] + "/")
        if timezone.now() + timedelta(days=1) > item.expire_token:
            print(item.book.file_link)
            # TODO download file but before upload to bucket s3 and edit file_link
            return HttpResponse(f"")
        else:
            return HttpResponse(f"Expire Link Download")


class HomeView(View):
    template_name = 'book/home.html'
    search_value = ''

    def get(self, request):
        page_number = self.request.GET.get('page')
        if 'search_value' in request.GET and request.GET['search_value']:
            search = request.GET['search_value']
            query_books = Book.objects.filter(title__icontains=search).order_by('title')
            if not query_books.exists():
                query_books = Book.objects.all()
                messages.warning(request, f'not found book for "{search}"', 'warning')
            else:
                messages.info(request, f'result text for "{search}" and found {query_books.count()} ', 'info')
                self.search_value = f'&search_value={search}'
        else:
            query_books = Book.objects.all()
        paginator = Paginator(query_books, 12)
        page_obj = paginator.get_page(page_number)
        return render(request, self.template_name, {'page_obj': page_obj, 'search_value': self.search_value})


class DetailBookView(View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=kwargs['book_id'])
        comments = Comment.objects.filter(book=book)
        return render(request, 'book/detail.html', {'book': book, 'comments': comments, 'comment_form': CommentForm})

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, id=kwargs['book_id'])
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                book=book,
                text=form.cleaned_data['text']
            )
            messages.info(request, 'your comment is save', 'success')
        comments = Comment.objects.filter(book=book)
        return render(request, 'book/detail.html', {'book': book, 'comments': comments, 'comment_form': CommentForm})


def form_search_book(request):
    return {'form_search': SearchBookForm}
