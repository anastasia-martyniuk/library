from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from catalog.forms import (
    LiteraryFormatForm,
    AuthorCreationForm,
    BookForm,
    BookSearchForm,
)
from catalog.models import Book, Author, LiteraryFormat


@login_required
def index(request):
    num_books = Book.objects.count()
    num_author = Author.objects.count()
    num_literary_formats = LiteraryFormat.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_books": num_books,
        "num_authors": num_author,
        "num_literary_formats": num_literary_formats,
        "num_visits": num_visits + 1,
    }

    return render(request, "catalog/index.html", context=context)


class LiteraryFormatListView(LoginRequiredMixin, generic.ListView):
    model = LiteraryFormat
    template_name = "catalog/literary_format_list.html"
    context_object_name = "literary_format_list"


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    queryset = Book.objects.all().select_related("format")
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)

        title = self.request.GET.get("title", "")

        context["search_form"] = BookSearchForm(initial={"title": title})

        return context

    def get_queryset(self):
        # title = self.request.GET.get("title")
        #
        # if title:
        #     return self.queryset.filter(title__icontains=title)
        #
        # return self.queryset

        form = BookSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(title__icontains=form.cleaned_data["title"])


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("catalog:book-list")


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy("catalog:book-list")


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author


class AuthorsCreateView(LoginRequiredMixin, generic.CreateView):
    model = Author
    form_class = AuthorCreationForm
    success_url = reverse_lazy("catalog:author-list")


def test_session_view(request):
    return HttpResponse(
        "<h1>Test Session</h1>" f"<h4>Session data: {request.session['book']}</h4>"
    )


class LiteraryFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = LiteraryFormat
    form_class = LiteraryFormatForm
    template_name = "catalog/literary_format_form.html"
    success_url = reverse_lazy("catalog:literary-format-list")


# def literary_formats_create(request):
#     context = {}
#     form = LiteraryFormatForm(request.POST or None)
#
#     if form.is_valid():
#         form.save()
#         # LiteraryFormat.objects.create(**form.cleaned_data)
#         return HttpResponseRedirect(reverse("catalog:literary-format-list"))
#
#     context["form"] = form
#     return render(request, "catalog/literary_format_form.html", context=context)

# if request.method == "GET":
#     context = {
#         "form": LiteraryFormatForm(),
#     }
#     return render(request, "catalog/literary_format_form.html", context=context)
#
# elif request.method == "POST":
#     form = LiteraryFormatForm(request.POST)
#
#     if form.is_valid():
#         LiteraryFormat.objects.create(**form.cleaned_data)
#         return HttpResponseRedirect(reverse("catalog:literary-format-list"))
#     context = {
#         "form": form
#     }
#
#     return render(request, "catalog/literary_format_form.html", context=context)


class LiteraryFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LiteraryFormat
    fields = "__all__"
    template_name = "catalog/literary_format_form.html"
    success_url = reverse_lazy("catalog:literary-format-list")


class LiteraryFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = LiteraryFormat
    template_name = "catalog/literary_format_confirm_delete.html"
    success_url = reverse_lazy("catalog:literary-format-list")
