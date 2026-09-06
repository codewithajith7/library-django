from django.contrib import admin
from django.utils.html import format_html
from app.models import Book

admin.site.site_header = "LibNexus Administration"
admin.site.site_title = "LibNexus Admin Portal"
admin.site.index_title = "Welcome to Library Management System Portal"

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'cover_preview', 'title', 'author', 'genre', 'isbn', 'price_display')
    list_filter = ('genre',)
    search_fields = ('title', 'author', 'isbn')
    ordering = ('-id',)
    list_per_page = 20

    def cover_preview(self, obj):
        if obj.cover:
            return format_html('<img src="{}" style="width: 40px; height: 52px; object-fit: cover; border-radius: 4px;" />', obj.cover.url)
        return "No Image"
    cover_preview.short_description = 'Cover'

    def price_display(self, obj):
        return f"${obj.price:.2f}"
    price_display.short_description = 'Price'
