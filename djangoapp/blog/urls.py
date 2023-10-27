from . import views
from django.urls import path

app_name = "blog"

urlpatterns = [
    path("", views.index, name="index"),
    path("post/<slug:slug>/", views.post, name="post"),
    path("page/<slug:slug>/", views.page, name="page"),
    path("created_by/<int:author_pk>/", views.created_by, name="created_by"),
    path("category/<slug:slug>/", views.category, name="category"),
    path("tag/<slug:slug>/", views.tag, name="tag"),
    path("search/", views.search, name="search"),
]
