from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from catalog.models import LiteraryFormat

LITERARY_FORMATS_URL = reverse("catalog:literary-format-list")


class PublicLiteraryFormatTests(TestCase):
    # def setUp(self) -> None:
    #     self.client = Client()

    def test_login_required(self):
        res = self.client.get(LITERARY_FORMATS_URL)

        self.assertNotEqual(res.status_code, 200)


class PrivateLiteraryFormatTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            "test",
            "password123"
        )
        self.client.force_login(self.user)

    def test_retrieve_literary_formats(self):
        LiteraryFormat.objects.create(name="poetry")
        LiteraryFormat.objects.create(name="drama")

        res = self.client.get(LITERARY_FORMATS_URL)

        literary_formats = LiteraryFormat.objects.all()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(
            list(res.context["literary_format_list"]),
            list(literary_formats)
        )
        self.assertTemplateUsed(res, "catalog/literary_format_list.html")
