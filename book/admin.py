from django.contrib import admin

from .models import Author,Publisher,Book

admin.site.register(Author)
admin.site.register(Publisher)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','publisher','size','published')
    list_filter = ('published',)
