from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock, EmailBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock

from app.core.models import LinkOrPageBlock


class JobOpportunitiesPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    header_text = RichTextField(blank=True)

    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)
    positions_title = models.CharField(default="Open Positions")
    sidebar_block_text = RichTextField(blank=True)

    rfp_banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="RFP banner image"
    )
    rfp_banner_title = models.CharField(default="Request for Proposals")
    rfp_banner_description = RichTextField(blank=True)
    rfp_banner_button_text = models.CharField(default="View all request for proposals")
    rfp_banner_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    red_box_title = models.CharField(default="HOT Salary Framework")
    red_box_description = RichTextField(blank=True)
    red_box_link_text = models.CharField(default="Salary Framework")
    red_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="Work Culture & Benefits")
    black_box_description = RichTextField(blank=True)
    black_box_link_text = models.CharField(default="Learn the benefits of working for HOT")
    black_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_text'),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('description'),
            FieldPanel('positions_title'),
            FieldPanel('sidebar_block_text'),
        ], heading="Main Body"),
        MultiFieldPanel([
            FieldPanel('rfp_banner_image'),
            FieldPanel('rfp_banner_title'),
            FieldPanel('rfp_banner_description'),
            FieldPanel('rfp_banner_button_text'),
            FieldPanel('rfp_banner_button_link'),
        ], heading="RFP Banner"),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_description'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_description'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Dogear Box"),
    ]
