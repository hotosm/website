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
    partner_is_active = models.BooleanField(default=True, help_text="If this field is unchecked, this partner will not appear in partner showcase carousels, nor the Our Partners page. They will, however, still appear in project pages that have them listed.")

    panels = [
        FieldPanel("partner_name"),
        FieldPanel("partner_logo"),
        FieldPanel("partner_url"),
        FieldPanel("partner_type"),
        FieldPanel("partner_is_active"),
    ]

    def __str__(self):
        return self.partner_name
    
    class Meta:
        verbose_name_plural = "Partners"


class LinkOrPageBlock(StreamBlock):
    page = PageChooserBlock()
    url = URLBlock()
    document = DocumentChooserBlock()
    other = CharBlock(help_text="Only use this option as a last resort. The other fields are preferred. In cases like email 'mailto' links, however, this field can be used. Ensure that your provided link will function as intended prior to publishing live.")

    class Meta:
        max_num = 1
