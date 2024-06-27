from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.search import index


class EventOwnerPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        keyword = request.GET.get('keyword', '')
        events_list = IndividualEventPage.objects.live().filter(locale=context['page'].locale)
        
        if keyword:
            events_list = events_list.search(keyword).get_queryset()
        
        match request.GET.get('sort', ''):
            case 'sort.new':
                events_list = events_list.order_by('-start_date_time')
            case 'sort.old':
                events_list = events_list.order_by('start_date_time')
            case 'sort.titlea':
                events_list = events_list.order_by('title')
            case 'sort.titlez':
                events_list = events_list.order_by('-title')
            case _:
                events_list = events_list.order_by('-start_date_time')

        page = request.GET.get('page', 1)
        paginator = Paginator(events_list, 6)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            events = paginator.page(page)
        except PageNotAnInteger:
            events = paginator.page(1)
        except EmptyPage:
            events = paginator.page(paginator.num_pages)
        
        context['events'] = events
        context['events_paginator'] = paginator
        context['current_page'] = int(page)
        return context
    
    max_count = 1

    event_location_title = models.CharField(default="Event Location")
    join_event_title = models.CharField(default="Join This Event")
    rsvp_button_text = models.CharField(default="RSVP")
    more_events_title = models.CharField(default="More Events")
    view_all_events_text = models.CharField(default="View all Events")
    view_all_events_url = models.URLField(blank=True)
    event_read_more_text = models.CharField(default="Read more")

    keyword_search_hint = models.CharField(default="Search by keyword")
    sort_by_new = models.CharField(default="Sort by New")
    sort_by_old = models.CharField(default="Sort by Old")
    sort_by_titlea = models.CharField(default="Sort by Title Alphabetical")
    sort_by_titlez = models.CharField(default="Sort by Title Reverse Alphabetical")
    search_button_text = models.CharField(default="Search")
    results_text = models.CharField(default="Results")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('keyword_search_hint'),
            FieldPanel('sort_by_new'),
            FieldPanel('sort_by_old'),
            FieldPanel('sort_by_titlea'),
            FieldPanel('sort_by_titlez'),
            FieldPanel('search_button_text'),
            FieldPanel('results_text'),
        ], heading="Event Search Page"),
        MultiFieldPanel([
            FieldPanel('event_location_title'),
            FieldPanel('join_event_title'),
            FieldPanel('rsvp_button_text'),
            FieldPanel('more_events_title'),
            FieldPanel('view_all_events_text'),
            FieldPanel('view_all_events_url'),
            FieldPanel('event_read_more_text'),
        ], heading="Individual Event Page"),
    ]


class IndividualEventPage(Page):
    parent_page_types = [
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

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('intro'),
    ]

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
