from django.urls import path

from catalog.views import (
    index,
    LiteraryFormatListView,
    BookListView,
    AuthorListView,
    BookDetailView,
    test_session_view,
    LiteraryFormatCreateView,
    LiteraryFormatUpdateView,
    LiteraryFormatDeleteView,
    AuthorsCreateView,
    BookCreateView,
    BookUpdateView,
)

urlpatterns = [
    path("", index, name="index"),
    path("test-session/", test_session_view, name="test-session"),
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),
    path("authors/", AuthorListView.as_view(), name="author-list"),
    path("authors/create/", AuthorsCreateView.as_view(), name="author-create"),
    path(
        "literary-formats/",
        LiteraryFormatListView.as_view(),
        name="literary-format-list",
    ),
    path(
        "literary-formats/create/",
        LiteraryFormatCreateView.as_view(),
        name="literary_format_create",
    ),
    path(
        "literary-formats/<int:pk>/update/",
        LiteraryFormatUpdateView.as_view(),
        name="literary-format-update",
    ),
    path(
        "literary-formats/<int:pk>/delete/",
        LiteraryFormatDeleteView.as_view(),
        name="literary-format-delete",
    ),
]

app_name = "catalog"
