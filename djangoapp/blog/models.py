from django.contrib.auth.models import User
from django.db import models
from utils.images import resize_image
from utils.rands import slugify_new


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True,
        default=None,
        null=True,
        blank=True,
        max_length=255,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.name)


class Page(models.Model):
    title = models.CharField(
        max_length=65,
    )
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )
    is_published = models.BooleanField(
        default=False,
        help_text=(
            "Este campo precisará estar marcado "
            "para a página ser exibida publicamente."
        ),
    )
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.title)


class Post(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    title = models.CharField(
        max_length=65,
    )
    slug = models.SlugField(
        unique=True, default="", null=False, blank=True, max_length=255
    )
    excerpt = models.CharField(max_length=255)
    is_published = models.BooleanField(
        default=False,
        help_text=(
            "Este campo precisará estar marcado "
            "para o post ser exibido publicamente."
        ),
    )
    content = models.TextField()
    cover = models.ImageField(
        upload_to="posts/%Y/%m",
        blank=True,
        default="",
    )
    cover_in_post_content = models.BooleanField(
        default=True,
        help_text="Se marcado, exibirá a capa dentro do post.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="post_created_by",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="page_updated_by",
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True, default=None
    )
    tags = models.ManyToManyField(Tag, blank=True, default="")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title, 4)
        current_cover_name = str(self.cover.name)
        super_save = super().save(*args, **kwargs)
        cover_changed = False
        if self.cover:
            cover_changed = current_cover_name != self.cover.name
        if cover_changed:
            resize_image(self.cover, 900)
        return super_save

    def __str__(self) -> str:
        return str(self.title)
