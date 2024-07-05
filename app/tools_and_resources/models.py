from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField


class LargePanel(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock()
    description = RichTextBlock()
    link_text = CharBlock()
    link_url = URLBlock(required=False)


class ToolsAndResourcesPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Intro image"
    )
    intro_header = models.CharField(blank=True)
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)
    learn_more_data_principles_text = models.CharField(default="Learn about our Data & Principles")
    learn_more_data_principles_link = models.URLField(blank=True)

    large_panels = StreamField([('panel', LargePanel())], use_json_field=True, null=True, blank=True)

    resource_learning_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Resource and Learning Centre image"
    )
    resource_learning_title = models.CharField(default="Resource and Learning Centre")
    resource_learning_description = RichTextField(blank=True)
    get_connected_button_text = models.CharField(default="Get connected now")
    get_connected_button_link = models.URLField(blank=True)

    dogear_tech_news_title = models.CharField(blank=True)
    dogear_tech_news_link_text = models.CharField(default="View our Tech News")
    dogear_tech_news_link_url = models.URLField(blank=True)

    red_box_title = models.CharField(default="Start Mapping")
    red_box_link_text = models.CharField(default="Start Mapping")
    red_box_link_url = models.URLField(null=True, blank=True)
    black_box_title = models.CharField(default="Check many opportunities to get involved with HOT!")
    black_box_link_text = models.CharField(default="Get Involved with HOT")
    black_box_link_url = models.URLField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        MultiFieldPanel([
            FieldPanel('intro_image'),
            FieldPanel('intro_header'),
            FieldPanel('intro'),
            FieldPanel('description'),
            FieldPanel('learn_more_data_principles_text'),
            FieldPanel('learn_more_data_principles_link'),
        ], heading="Intro"),
        FieldPanel('large_panels'),
        MultiFieldPanel([
            FieldPanel('resource_learning_image'),
            FieldPanel('resource_learning_title'),
            FieldPanel('resource_learning_description'),
            FieldPanel('get_connected_button_text'),
            FieldPanel('get_connected_button_link'),
        ], heading="Resource and Learning Centre"),
        MultiFieldPanel([
            FieldPanel('dogear_tech_news_title'),
            FieldPanel('dogear_tech_news_link_text'),
            FieldPanel('dogear_tech_news_link_url'),
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Dogear Boxes"),
    ]
