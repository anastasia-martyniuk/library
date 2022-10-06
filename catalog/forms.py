from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from catalog.models import LiteraryFormat, Author, Book


#
#
# class LiteraryFormatForm(forms.ModelForm):
#     class Meta:
#         model = LiteraryFormat
#         fields = "__all__"


class LiteraryFormatForm(forms.ModelForm):
    MIN_WORD_COUNT = 19000

    word_count = forms.IntegerField(
        required=True, validators=[MinValueValidator(MIN_WORD_COUNT)]
    )

    class Meta:
        model = LiteraryFormat
        fields = ("name", "word_count", "annotation")

    # def clean_word_count(self):
    #     word_count = self.cleaned_data["word_count"]
    #
    #     if word_count < LiteraryFormatForm.MIN_WORD_COUNT:
    #         raise ValidationError(f"Ensure that value is >= {LiteraryFormatForm.MIN_WORD_COUNT}")
    #
    #     return word_count


class AuthorCreationForm(UserCreationForm):
    class Meta:
        model = Author
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "pseudonym",
        )


class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = Book
        fields = "__all__"


class BookSearchForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by title"}),
    )
