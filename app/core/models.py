from django import forms
from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel


class ErrorPage(Page):
    max_count = 1


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
    partner_type = StreamField([('type', PageChooserBlock(page_type="partners.PartnershipTemplatePage"))], use_json_field=True, null=True, blank=True)

    panels = [
        FieldPanel("partner_name"),
        FieldPanel("partner_logo"),
        FieldPanel("partner_url"),
        FieldPanel("partner_type"),
    ]

    def __str__(self):
        return self.partner_name
    
    class Meta:
        verbose_name_plural = "Partners"


class LinkOrPageBlock(StreamBlock):
    page = PageChooserBlock()
    url = URLBlock()
    document = DocumentChooserBlock()

    class Meta:
        max_num = 1
