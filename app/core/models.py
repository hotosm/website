from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField

from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel


@register_snippet
class Partner(models.Model):
    partner_name = models.CharField()
    partner_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Partner logo"
    )
    partner_url = models.URLField(blank=True)

    panels = [
        FieldPanel("partner_name"),
        FieldPanel("partner_logo"),
        FieldPanel("partner_url"),
    ]

    def __str__(self):
        return self.partner_name
    
    class Meta:
        verbose_name_plural = "Partners"


class HotSearchablePage(Page):
    pass
