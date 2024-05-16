from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock


class IndividualProjectPage(Page):
    # > HEADER
    owner_program = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    location = models.CharField(blank=True)
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    # > BODY
    intro = RichTextField(blank=True)
    description = StreamField([
        ('text_block', RichTextBlock(features=[
        'h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ]))
    ], use_json_field=True, null=True)

    call_to_action_title = models.CharField(default="Call to Action")
    call_to_action_description = RichTextField(null=True, blank=True)
    call_to_action_link_text = models.CharField(default="Call to Action Link")
    call_to_action_link_url = models.URLField(null=True, blank=True)

    # > SIDE BAR
    impact_areas_title = models.CharField(default="Impact Areas")
    impact_areas = RichTextField(null=True, blank=True)  # Will need to reference an impact area once impact areas are added
    
    region_hub_title = models.CharField(default="Region Hub")
    region_hub = RichTextField(null=True, blank=True)  # Will need to reference a region hub when region hubs are added
    
    duration_title = models.CharField(default="Duration")
    duration = models.CharField(default="Ongoing", blank=True)
    
    partners_title = models.CharField(default="Partners")
    partners = RichTextField(null=True, blank=True)  # Will need to reference partners when they are added
    
    tools_title = models.CharField(default="Tools")
    tools = RichTextField(null=True, blank=True)  # Will need to reference tools when they are added
    
    contact_title = models.CharField(default="Contact")
    contact = RichTextField(null=True, blank=True)

    # Question: are related news/events chosen for the article, or are they based off something?
    related_news_title = models.CharField(default="Related News")
    view_all_news_text = models.CharField(default="View all News")
    related_news = StreamField([
        ('news_page', PageChooserBlock(page_type="news.IndividualNewsPage"))
    ], use_json_field=True, null=True, blank=True)

    related_events_title = models.CharField(default="Related Events")
    view_all_events_text = models.CharField(default="View all Events")

    # > BOTTOM AREA
    red_box_title = models.CharField(default="Chat with Our Community")
    red_box_link_text = RichTextField(default="Get connected now")
    red_box_link_url = models.URLField(null=True, blank=True)
    black_box_title = models.CharField(default="Our Work")
    black_box_link_text = RichTextField(default="View Our Work")
    black_box_link_url = models.URLField(null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            PageChooserPanel('owner_program', 'programs.IndividualProgramPage'),
            FieldPanel('location'),
            FieldPanel('header_image')
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('description'),
            MultiFieldPanel([
                FieldPanel('call_to_action_title'),
                FieldPanel('call_to_action_description'),
                FieldPanel('call_to_action_link_text'),
                FieldPanel('call_to_action_link_url'),
            ], heading="Call to Action"),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('impact_areas_title'),
            FieldPanel('impact_areas'),
            FieldPanel('region_hub_title'),
            FieldPanel('region_hub'),
            FieldPanel('duration_title'),
            FieldPanel('duration'),
            FieldPanel('partners_title'),
            FieldPanel('partners'),
            FieldPanel('tools_title'),
            FieldPanel('tools'),
            FieldPanel('contact_title'),
            FieldPanel('contact'),
            FieldPanel('related_news_title'),
            FieldPanel('view_all_news_text'),
            FieldPanel('related_news'),
            FieldPanel('related_events_title'),
            FieldPanel('view_all_events_text'),
        ], heading="Sidebar"),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Bottom")
    ]