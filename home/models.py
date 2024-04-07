from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.models import Page


class HomePage(Page):
    templates = "home/home_page.html"

    # Hero section
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Banner image",
    )
    hero_text = models.CharField(
        max_length=500,
        blank=False,
        null=True,
        help_text="Write an introduction for the hero/landing page section",
    )
    hero_cta = models.CharField(
        max_length=50, blank=False, null=True, help_text="Write text for the Call to Action button"
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Select a page to link to for the Call to Action button",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("image"),
                FieldPanel("hero_text"),
                FieldPanel("hero_cta"),
                FieldPanel("hero_cta_link"),
            ],
            heading="Hero Section",
        ),
    ]
