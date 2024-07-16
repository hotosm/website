from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.models import Page


class VolunteerOpportunityOwnerPage(Page):
    subpage_types = [
        'volunteer_opportunities.IndividualVolunteerOpportunityPage'
    ]

    max_count = 1

    posted_by_prefix_text = models.CharField(default="Posted by")
    
    contact_title = models.CharField(default="Contact")
    application_date_title = models.CharField(default="Application Date")
    location_title = models.CharField(default="Location")

    share_text = models.CharField(default="Share")
    go_back_text = models.CharField(default="Go Back to Volunteer Opportunities")

    content_panels = Page.content_panels + [
        FieldPanel('posted_by_prefix_text'),
        MultiFieldPanel([
            FieldPanel('contact_title'),
            FieldPanel('application_date_title'),
            FieldPanel('location_title'),
        ], heading="Sidebar"),
        MultiFieldPanel([
            FieldPanel('share_text'),
            FieldPanel('go_back_text'),
        ], heading="Bottom"),
    ]


class IndividualVolunteerOpportunityPage(Page):
    parent_page_type = [
        'volunteer_opportunities.VolunteerOpportunityOwnerPage'
    ]

    posters = StreamField([('poster', PageChooserBlock(page_type="members.IndividualMemberPage"))], use_json_field=True, null=True, blank=True)

    intro = RichTextField(blank=True)
    article_body = StreamField([
        ('text_block', RichTextBlock(features=[
        'h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ]))
    ], use_json_field=True, null=True, blank=True)

    contact_description = RichTextField(blank=True)
    application_description = RichTextField(blank=True)
    application_date = models.DateField()
    location_text = models.CharField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('posters'),
        FieldPanel('intro'),
        FieldPanel('article_body'),
        MultiFieldPanel([
            FieldPanel('contact_description'),
            FieldPanel('application_description'),
            FieldPanel('application_date'),
            FieldPanel('location_text'),
        ], heading="Sidebar"),
    ]
