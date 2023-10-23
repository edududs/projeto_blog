from blog.models import Category, Page, Post, Tag
from django.contrib import admin


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = ("name",)
    search_fields = (
        "id",
        "name",
        "slug",
    )
    list_per_page = 10
    ordering = ("-id",)
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
    )
    list_display_links = ("name",)
    search_fields = (
        "id",
        "name",
        "slug",
    )
    list_per_page = 10
    ordering = ("-id",)
    prepopulated_fields = {
        "slug": ("name",),
    }


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "is_published",
    )
    list_display_links = ("title",)
    search_fields = (
        "id",
        "slug",
        "title",
        "content",
    )
    list_per_page = 50
    list_filter = ("is_published",)
    list_editable = ("is_published",)
    ordering = ("-id",)
    prepopulated_fields = {
        "slug": ("title",),
    }


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "is_published",
        "created_by",
    )
    list_display_links = ("title",)
    search_fields = (
        "id",
        "slug",
        "title",
        "content",
        "excerpt",
    )
    list_per_page = 50
    list_filter = (
        "category",
        "is_published",
    )
    list_editable = ("is_published",)
    ordering = ("-id",)
    readonly_fields = (
        "created_at",
        "updated_at",
        "updated_by",
        "created_by",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    autocomplete_fileds = (
        "tags",
        "category",
    )

    def save_model(self, request, obj, form, change):
        if change:
            obj.updated_by = request.user
        else:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)