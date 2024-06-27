from django import forms
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField


"""
This page should only be created as a child of an IndividualMappingHubPage!
Its template depends on fields from the IndividualMappingHubPage in order
to create one unifying place where unchanging fields may be modified.
"""
class ProjectOwnerPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        projects_list = context['page'].get_children().filter(locale=context['page'].locale)
        page = request.GET.get('page', 1)
        paginator = Paginator(projects_list, 8)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)
        context['projects'] = projects
        return context
    
    parent_page_types = [
        'mapping_hubs.IndividualMappingHubPage'
    ]

    subpage_types = [
        'projects.IndividualProjectPage'
    ]

    load_more_projects_text = models.CharField(default="Load More Projects")

    impact_areas_title = models.CharField(default="Impact Areas")
    region_hub_title = models.CharField(default="Region Hub")
    duration_title = models.CharField(default="Duration")
    partners_title = models.CharField(default="Partners")
    tools_title = models.CharField(default="Tools")
    contact_title = models.CharField(default="Contact")

    related_news_title = models.CharField(default="Related News")
    view_all_news_text = models.CharField(default="View all News")
    view_all_news_url = models.URLField(blank=True)
    related_events_title = models.CharField(default="Related Events")
    view_all_events_text = models.CharField(default="View all Events")
    view_all_events_url = models.URLField(blank=True)

    red_box_title = models.CharField(default="Chat with Our Community")
    red_box_link_text = models.CharField(default="Get connected now")
    red_box_link_url = models.URLField(null=True, blank=True)
    black_box_title = models.CharField(default="Our Work")
    black_box_link_text = models.CharField(default="View Our Work")
    black_box_link_url = models.URLField(null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('load_more_projects_text'),
        ], heading="Project Open Mapping Hub Page"),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('impact_areas_title'),
                FieldPanel('region_hub_title'),
                FieldPanel('duration_title'),
                FieldPanel('partners_title'),
                FieldPanel('tools_title'),
                FieldPanel('contact_title'),
                MultiFieldPanel([
                    FieldPanel('related_news_title'),
                    FieldPanel('view_all_news_text'),
                    FieldPanel('view_all_news_url'),
                    FieldPanel('related_events_title'),
                    FieldPanel('view_all_events_text'),
                    FieldPanel('view_all_events_url'),
                ], heading="Related Pages"),
            ], heading="Sidebar"),
            MultiFieldPanel([
                FieldPanel('red_box_title'),
                FieldPanel('red_box_link_text'),
                FieldPanel('red_box_link_url'),
                FieldPanel('black_box_title'),
                FieldPanel('black_box_link_text'),
                FieldPanel('black_box_link_url'),
            ], heading="Footer"),
        ], heading="Individual Project Page"),
    ]


"""
This page should only be created as a child of a ProjectOwnerPage!
Its template depends on fields from the ProjectOwnerPage in order
to create one unifying place where unchanging fields may be modified.
"""
class IndividualProjectPage(Page):
    parent_page_types = [
        'projects.ProjectOwnerPage'
    ]
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
        'h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ]))
    ], use_json_field=True, null=True)

    call_to_action_title = models.CharField(default="Call to Action")
    call_to_action_description = RichTextField(null=True, blank=True)
    call_to_action_link_text = models.CharField(default="Call to Action Link")
    call_to_action_link_url = models.URLField(null=True, blank=True)

    # > SIDE BAR
    impact_area_list = StreamField([('impact_area', PageChooserBlock(page_type="impact_areas.IndividualImpactAreaPage"))], use_json_field=True, null=True, blank=True)
    
    duration = models.CharField(default="Ongoing", blank=True)
    
    partners_list = ParentalManyToManyField('core.Partner', blank=True)
    
    tools = RichTextField(null=True, blank=True)  # Will need to reference tools when they are added
    
    contact = RichTextField(null=True, blank=True)

    related_news = StreamField([
        ('news_page', PageChooserBlock(page_type="news.IndividualNewsPage"))
    ], use_json_field=True, null=True, blank=True)

    related_events = StreamField([
        ('event_page', PageChooserBlock(page_type="events.IndividualEventPage"))
    ], use_json_field=True, null=True, blank=True)

    project_contributors = StreamField([('contributor', PageChooserBlock(page_type="members.IndividualMemberPage"))], use_json_field=True, null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            PageChooserPanel('owner_program', 'programs.IndividualProgramPage'),
            FieldPanel('location'),
            FieldPanel('header_image'),
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
            FieldPanel('impact_area_list'),
            FieldPanel('duration'),
            FieldPanel('partners_list', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tools'),
            FieldPanel('contact'),
            MultiFieldPanel([
                FieldPanel('related_news'),
                FieldPanel('related_events'),
            ], heading="Related Pages"),
        ], heading="Sidebar"),
        MultiFieldPanel([
            FieldPanel('project_contributors'),
        ], heading="Extras")
    ]