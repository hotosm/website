from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField


class EventOwnerPage(Page):
    max_count = 1

    event_location_title = models.CharField(default="Event Location")
    join_event_title = models.CharField(default="Join This Event")
    rsvp_button_text = models.CharField(default="RSVP")
    more_events_title = models.CharField(default="More Events")
    view_all_events_text = models.CharField(default="View all Events")
    view_all_events_url = models.URLField(blank=True)
    event_read_more_text = models.CharField(default="Read more")

    content_panels = Page.content_panels + [
        FieldPanel('event_location_title'),
        FieldPanel('join_event_title'),
        FieldPanel('rsvp_button_text'),
        FieldPanel('more_events_title'),
        FieldPanel('view_all_events_text'),
        FieldPanel('view_all_events_url'),
        FieldPanel('event_read_more_text'),
    ]


class IndividualEventPage(Page):
    parent_page_type = [
        'projects.ProjectOwnerPage'
    ]

    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Image to represent the event"
    )
    intro = RichTextField(blank=True)
    extended_description = StreamField([
        ('text_block', RichTextBlock(features=[
        'h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ]))
    ], use_json_field=True, null=True)

    event_location = models.CharField(blank=True)
    rsvp_description = RichTextField(blank=True, help_text="If this field is empty, the RSVP description will not appear.")
    rsvp_link = models.URLField(blank=True, help_text="If this field is empty, the RSVP button will not appear. If both RSVP Description and Link are empty, the RSVP section will be hidden.")

    more_events = StreamField([
        ('event', PageChooserBlock(page_type="events.IndividualEventPage"))
    ], use_json_field=True, null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('start_date_time'),
            FieldPanel('end_date_time'),
        ], heading="Date and Time"),
        MultiFieldPanel([
            FieldPanel('image'),
            FieldPanel('intro'),
            FieldPanel('extended_description'),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('event_location'),
            FieldPanel('rsvp_description'),
            FieldPanel('rsvp_link'),
            FieldPanel('more_events'),
        ], heading="Sidebar")
    ]
