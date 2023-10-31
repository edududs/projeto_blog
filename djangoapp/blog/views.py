from typing import Any

from blog.models import Page, Post
from django import http
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models
from django.db.models.query import QuerySet
from django.db.models.query_utils import Q
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

PER_PAGE = 9


class PostListView(ListView):
    model = Post
    template_name = "blog/pages/index.html"
    context_object_name = "posts"
    ordering = "-created_at"
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context.update(
            {
                "page_title": "Home - ",
            }
        )
        return context


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        user = self._temp_context["user"]
        user_full_name = user.username
        if user.first_name:
            user_full_name = f"{user.first_name} {user.last_name}"
        page_title = f"Posts de {user_full_name}  - "
        ctx.update({"page_title": page_title})

        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(created_by__pk=self._temp_context["user"].pk)
        return qs

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        author_pk = self.kwargs.get("author_pk")
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({"author_pk": author_pk, "user": user})

        return super().get(request, *args, **kwargs)


# def created_by(request, author_pk):
#     user = User.objects.filter(pk=author_pk).first()
#     if user is None:
#         raise Http404()
#     posts = Post.objects.get_published().filter(created_by__pk=author_pk)
#     user_full_name = user.username
#     if user.first_name:
#         user_full_name = f"{user.first_name} {user.last_name}"
#     page_title = f"Posts de {user_full_name}  - "

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     return render(
#         request,
#         "blog/pages/index.html",
#         {
#             "page_obj": page_obj,
#             "page_title": page_title,
#         },
#     )


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(category__slug=self.kwargs.get("slug"))
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].category.name} - Categoria - "
        ctx.update({"page_title": page_title})
        return ctx


# def category(request, slug):
#     posts = Post.objects.get_published().filter(category__slug=slug)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f"{page_obj[0].category.name} - Categoria -"

#     return render(
#         request,
#         "blog/pages/index.html",
#         {
#             "page_obj": page_obj,
#             "page_title": page_title,
#         },
#     )


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset().filter(tags__slug=self.kwargs.get("slug"))
        return qs

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].tags.first().name} - Tag - "
        ctx.update({"page_title": page_title})
        return ctx


# def tag(request, slug):
#     posts = Post.objects.get_published().filter(tags__slug=slug)

#     paginator = Paginator(posts, PER_PAGE)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:
#         raise Http404()

#     page_title = f"{page_obj[0].tags.first().name} - Tag -"

#     return render(
#         request,
#         "blog/pages/index.html",
#         {
#             "page_obj": page_obj,
#             "page_title": page_title,
#         },
#     )


class SearchListView(PostListView):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._search_value = ""

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        search_value = self._search_value
        return (
            super()
            .get_queryset()
            .filter(
                Q(title__icontains=search_value)
                | Q(content__icontains=search_value)
                | Q(excerpt__icontains=search_value)
            )[:PER_PAGE]
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page_title = f"{self._search_value[:15]} - Search - "
        search_value = self._search_value
        ctx.update({"search_value": search_value, "page_title": page_title})
        return ctx

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if self._search_value == "":
            return redirect("blog:index")
        return super().get(request, *args, **kwargs)


# def search(request):
#     search_value = request.GET.get("search", "").strip()
#     posts = Post.objects.get_published().filter(
#         Q(title__icontains=search_value)
#         | Q(content__icontains=search_value)
#         | Q(excerpt__icontains=search_value)
#     )[:PER_PAGE]

#     page_title = f"{search_value[:15]} - Search -"

#     return render(
#         request,
#         "blog/pages/index.html",
#         {
#             "page_obj": posts,
#             "search_value": search_value,
#             "page_title": page_title,
#         },
#     )


class PageDetailView(DetailView):
    model = Page
    template_name = "blog/pages/page.html"
    slug_field = "slug"
    context_object_name = "page"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f"{page.title} - Página - "
        ctx.update({"page_title": page_title})
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


# def page(request, slug):
#     page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()

#     if page_obj is None:
#         raise Http404()

#     page_title = f"{page_obj.title} - Página -"

#     return render(
#         request,
#         "blog/pages/page.html",
#         {
#             "page": page_obj,
#             "page_title": page_title,
#         },
#     )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/pages/post.html"
    slug_field = "slug"
    context_object_name = "page"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        ctx = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f"{post.title} - Post - "
        ctx.update({"page_title": page_title})
        return ctx

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


# def post(request, slug):
#     post_obj = Post.objects.get_published().filter(slug=slug).first()

#     if post_obj is None:
#         raise Http404()

#     page_title = f"{post_obj.title} - Post -"

#     return render(
#         request,
#         "blog/pages/post.html",
#         {
#             "post": post_obj,
#             "page_title": page_title,
#         },
#     )
