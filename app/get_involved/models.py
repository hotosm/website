from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField


class GetInvolvedLargePanel(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock()
    description = RichTextBlock()
    link_text = CharBlock()
    link_url = URLBlock(required=False)


class JoinUsPanel(StructBlock):
    image = ImageChooserBlock()
    page = PageChooserBlock()
    tablet_description = RichTextBlock(required=False, blank=True)


class GetInvolvedPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    partner_with_us_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    partner_with_us_title = models.CharField(default="Partner With Us!")
    partner_with_us_description = RichTextField(blank=True)
    partner_with_us_button_text = models.CharField(default="Partner With Us")
    partner_with_us_button_link = models.URLField(blank=True)

    get_involved_community_title = models.CharField(default="Get Involved in Our Community")
    get_involved_large_panels = StreamField([('panel', GetInvolvedLargePanel())], use_json_field=True, blank=True, null=True)
    dogear_box_title = models.CharField(default="Connect with our OSM community!")
    dogear_box_link_text = models.CharField(default="Contact by Country")
    dogear_box_link_url = models.URLField(blank=True)
    events_title = models.CharField(default="Events")
    view_all_events_text = models.CharField(default="View all Events")
    view_all_events_link = models.URLField(blank=True)
    events = StreamField([('event', PageChooserBlock(page_type="events.IndividualEventPage"))], use_json_field=True, null=True, blank=True, max_num=3)

    join_us_title = models.CharField(default="Join Us")
    join_us_panels = StreamField([('panel', JoinUsPanel())], use_json_field=True, blank=True, null=True)
    join_us_panel_read_more = models.CharField(default="Read More")
    red_box_title = models.CharField(default="Support HOT's work!")
    red_box_link_text = models.CharField(default="Donate Today")
    red_box_link_url = models.URLField(null=True, blank=True)
    black_box_title = models.CharField(default="Stay in Touch")
    black_box_link_text = models.CharField(default="Contact Us")
    black_box_link_url = models.URLField(null=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        MultiFieldPanel([
            FieldPanel('partner_with_us_image'),
            FieldPanel('partner_with_us_title'),
            FieldPanel('partner_with_us_description'),
            FieldPanel('partner_with_us_button_text'),
            FieldPanel('partner_with_us_button_link'),
        ], heading="Partner With Us"),
        MultiFieldPanel([
            FieldPanel('get_involved_community_title'),
            FieldPanel('get_involved_large_panels'),
            FieldPanel('dogear_box_title'),
            FieldPanel('dogear_box_link_text'),
            FieldPanel('dogear_box_link_url'),
            FieldPanel('events_title'),
            FieldPanel('view_all_events_text'),
            FieldPanel('view_all_events_link'),
            FieldPanel('events'),
        ], heading="Get Involved in Our Community"),
        MultiFieldPanel([
            FieldPanel('join_us_title'),
            FieldPanel('join_us_panels'),
            FieldPanel('join_us_panel_read_more'),
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Bottom Area"),
    ]
