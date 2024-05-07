from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import StreamBlock, CharBlock, URLBlock, RichTextBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


class IndividualBlock(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock()
    description = RichTextBlock()
    link = URLBlock(required=False)


class ImpactAreaBlock(StreamBlock):
    impact_area_block = IndividualBlock()


class ImpactAreasPage(Page):
    intro = RichTextField(blank=True)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    impact_area_blocks = StreamField(ImpactAreaBlock(), use_json_field=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('image'),
            FieldPanel('intro')
        ], heading="Header section"),
        FieldPanel('impact_area_blocks')
    ]
