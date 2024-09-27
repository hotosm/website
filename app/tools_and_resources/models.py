from django import forms
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from app.core.models import LinkOrPageBlock


class LargePanel(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock()
    description = RichTextBlock()
    link_text = CharBlock()
    link = LinkOrPageBlock(required=False)


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
    learn_more_data_principles_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

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
    get_connected_button_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    dogear_tech_news_title = models.CharField(blank=True)
    dogear_tech_news_link_text = models.CharField(default="View our Tech News")
    dogear_tech_news_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    category_filter_selector = models.ForeignKey(
        "news.NewsCategory",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The 'Tech News' link will be appended with a filter for this category. The selected category should be the Tech category."
    )

    red_box_title = models.CharField(default="Start Mapping")
    red_box_link_text = models.CharField(default="Start Mapping")
    red_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="Check many opportunities to get involved with HOT!")
    black_box_link_text = models.CharField(default="Get Involved with HOT")
    black_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        MultiFieldPanel([
            FieldPanel('intro_image'),
            FieldPanel('intro_header'),
            FieldPanel('intro'),
            FieldPanel('description'),
            FieldPanel('learn_more_data_principles_text'),
            FieldPanel('learn_more_data_principles_url'),
        ], heading="Intro"),
        FieldPanel('large_panels'),
        MultiFieldPanel([
            FieldPanel('resource_learning_image'),
            FieldPanel('resource_learning_title'),
            FieldPanel('resource_learning_description'),
            FieldPanel('get_connected_button_text'),
            FieldPanel('get_connected_button_url'),
        ], heading="Resource and Learning Centre"),
        MultiFieldPanel([
            FieldPanel('dogear_tech_news_title'),
            FieldPanel('dogear_tech_news_link_text'),
            FieldPanel('dogear_tech_news_link'),
            FieldPanel('category_filter_selector', widget=forms.RadioSelect),
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link'),
        ], heading="Dogear Boxes"),
    ]


class ResourceAndLearningPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    intro = RichTextField(blank=True)

    large_panels = StreamField([('panel', LargePanel())], use_json_field=True, null=True, blank=True)
    
    go_back_prefix_text = models.CharField(default="Go Back to")
    
    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('large_panels'),
        FieldPanel('go_back_prefix_text'),
    ]


class OpenMappingSolutionIndividualItemBlock(StructBlock):
    title = CharBlock()
    description = RichTextBlock()
    links = StreamBlock([
        ('link', StructBlock([
            ('linktext', CharBlock()),
            ('linkurl', LinkOrPageBlock(required=False)),
        ]))
    ], required=False)


class OpenMappingSolutionBlock(StructBlock):
    title = CharBlock()
    banner = ImageChooserBlock()
    description = RichTextBlock()
    items = StreamBlock([('item', OpenMappingSolutionIndividualItemBlock())])


class OpenMappingSolutionsPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    intro = RichTextField(blank=True)

    solutions = StreamField([('solution',OpenMappingSolutionBlock())], use_json_field=True, blank=True, null=True)

    cta_title = models.CharField(default="Get Started with Open Mapping")
    cta_description = RichTextField(blank=True)
    cta_button_text = models.CharField(default="Start Open Mapping")
    cta_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    go_back_prefix_text = models.CharField(default="Go Back to")

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('solutions'),
        FieldPanel('cta_title'),
        FieldPanel('cta_description'),
        FieldPanel('cta_button_text'),
        FieldPanel('cta_button_link'),
        FieldPanel('go_back_prefix_text'),
    ]
