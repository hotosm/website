from django.core.management.base import BaseCommand
from django.db import transaction
from wagtail.contrib.redirects.models import Redirect
from wagtail.models import Page

from app.misc.models import DocumentCollectionPage, WorkingGroupsPage
from home.models import HomePage

PDF_V2_URL = "https://hotosm.github.io/hotosm-website/downloads/ActivationProtocolV2.pdf"
PDF_V1_URL = "https://hotosm.github.io/hotosm-website/downloads/HOTActivationProtocol.pdf"
PAGE_SLUG = "hot-activation-protocol"
LEGACY_REDIRECT_PATHS = (
    "/hot-activation-protocol",
    "/hot-activation-protocol/",
    "/activation_protocol",
    "/activation_protocol/",
)


def _url_link(url: str) -> list[dict]:
    return [{"type": "url", "value": url}]


def _find_working_groups_page() -> Page | None:
    return WorkingGroupsPage.objects.live().first()


class Command(BaseCommand):
    help = "Create the HOT Activation Protocol page and legacy URL redirects."

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace-pdf-redirect",
            action="store_true",
            help="Replace any existing redirect that points directly at the PDF.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        home = HomePage.objects.live().first()
        if not home:
            self.stderr.write(self.style.ERROR("No live HomePage found."))
            return

        page = DocumentCollectionPage.objects.filter(slug=PAGE_SLUG).first()
        working_groups = _find_working_groups_page()
        working_groups_html = (
            f'<p><a href="{working_groups.url}">Read more</a> about the Activation '
            "and other HOT working groups about getting involved.</p>"
            if working_groups
            else (
                "<p>Read more about the Activation and other HOT working groups "
                "about getting involved.</p>"
            )
        )

        page_fields = {
            "title": "HOT Activation Protocol",
            "slug": PAGE_SLUG,
            "header_description": (
                "<p>Download the HOT Activation Protocol documents and learn how "
                "HOT coordinates disaster mapping activations.</p>"
                + working_groups_html
            ),
            "document_access_prefix_text": "Download",
            "documents": [
                {
                    "type": "block",
                    "value": {
                        "title": "Activation Protocol Version 2 (2022)",
                        "link": _url_link(PDF_V2_URL),
                        "description": "<p><strong>Available Now!</strong></p>",
                    },
                },
                {
                    "type": "block",
                    "value": {
                        "title": "Original Activation Protocol (2015)",
                        "link": _url_link(PDF_V1_URL),
                        "description": "",
                    },
                },
            ],
            "sidebar_box_title": "Have a question about the activation protocol?",
            "sidebar_box_button_text": "Contact Activation Working Group",
            "sidebar_box_button_link": [
                {"type": "other", "value": "mailto:activation@hotosm.org"},
            ],
        }

        if page:
            for field, value in page_fields.items():
                setattr(page, field, value)
            page.save_revision().publish()
            self.stdout.write(self.style.WARNING(f"Updated existing page: {page.url}"))
        else:
            page = DocumentCollectionPage(**page_fields)
            home.add_child(instance=page)
            page.save_revision().publish()
            self.stdout.write(self.style.SUCCESS(f"Created page: {page.url}"))

        for old_path in LEGACY_REDIRECT_PATHS:
            redirect, created = Redirect.objects.update_or_create(
                old_path=old_path,
                defaults={
                    "site": page.get_site(),
                    "redirect_page": page,
                    "link": None,
                    "is_permanent": True,
                },
            )
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} redirect: {old_path} -> {page.url}")

        if options["replace_pdf_redirect"]:
            replaced = Redirect.objects.filter(link=PDF_V2_URL).update(
                redirect_page=page,
                link=None,
                is_permanent=True,
            )
            if replaced:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Replaced {replaced} PDF redirect(s) with page redirect."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Done. Review in Wagtail admin before removing the temporary PDF redirect."
            )
        )
