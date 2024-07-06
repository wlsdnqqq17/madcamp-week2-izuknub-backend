from django.contrib import admin
from .models import Author, Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birthdate')
    search_fields = ('first_name', 'last_name')

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'isbn')
    search_fields = ('title', 'isbn')
    list_filter = ('published_date', 'author')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
