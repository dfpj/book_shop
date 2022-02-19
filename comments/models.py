from django.db import models
from django.conf import settings
from book.models import Book
from django.conf import settings


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'{self.user} {self.text[:30]}'

    def count_like(self):
        return self.like_comment_comments.count()


class LikeComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='like_user_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='like_comment_comments')

    def __str__(self):
        return f'{self.user}'



