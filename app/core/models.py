from django import forms
from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel


@register_snippet
class PartnerType(models.Model):
    type_name = models.CharField()

    panels = [
        FieldPanel("type_name")
    ]

    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Partner Types"


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
    partner_type = models.ForeignKey(
        'core.PartnerType',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel("partner_name"),
        FieldPanel("partner_logo"),
        FieldPanel("partner_url"),
        FieldPanel("partner_type", widget=forms.RadioSelect),
    ]

    def __str__(self):
        return self.partner_name
    
    class Meta:
        verbose_name_plural = "Partners"


class LinkOrPageBlock(StreamBlock):
    page = PageChooserBlock()
    url = URLBlock()

    class Meta:
        max_num = 1
