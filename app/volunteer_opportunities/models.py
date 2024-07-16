from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.models import Page


class VolunteerOpportunityOwnerPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        opportunities = IndividualVolunteerOpportunityPage.objects.live().filter(locale=context['page'].locale)
        
        context['opportunities'] = opportunities
        return context
    
    subpage_types = [
        'volunteer_opportunities.IndividualVolunteerOpportunityPage'
    ]

    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    header_description = RichTextField(blank=True)

    intro = RichTextField(blank=True)
    body_description = RichTextField(blank=True)
    open_opportunities_title = models.CharField(default="Open Opportunities")
    open_opportunities_location_text = models.CharField(default="Location")
    open_opportunities_deadline_text = models.CharField(default="Deadline")
    open_opportunities_learn_more_text = models.CharField(default="Learn More")
    no_opportunities_title = models.CharField(default="There are no current openings.")
    no_opportunities_description = RichTextField(blank=True)

    aside_block_title = models.CharField(default="Didn't find the volunteer opportunity you were looking for?")
    aside_block_description = RichTextField(blank=True)
    aside_block_link_text = models.CharField(default="Contact us")
    aside_block_link_url = models.URLField(blank=True)

    red_box_title = models.CharField(default="Join our Slack channel and find more opportunities")
    red_box_link_text = models.CharField(default="Join our conversation")
    red_box_link_url = models.URLField(null=True, blank=True)
    black_box_title = models.CharField(default="Check out upcoming events")
    black_box_link_text = models.CharField(default="See our events")
    black_box_link_url = models.URLField(null=True, blank=True)

    posted_by_prefix_text = models.CharField(default="Posted by")
    
    contact_title = models.CharField(default="Contact")
    application_date_title = models.CharField(default="Application Date")
    location_title = models.CharField(default="Location")

    share_text = models.CharField(default="Share")
    go_back_text = models.CharField(default="Go Back to Volunteer Opportunities")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_description'),
        ], heading="Heading"),
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body_description'),
            FieldPanel('open_opportunities_title'),
            FieldPanel('open_opportunities_location_text'),
            FieldPanel('open_opportunities_deadline_text'),
            FieldPanel('open_opportunities_learn_more_text'),
            FieldPanel('no_opportunities_title'),
            FieldPanel('no_opportunities_description'),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('aside_block_title'),
            FieldPanel('aside_block_description'),
            FieldPanel('aside_block_link_text'),
            FieldPanel('aside_block_link_url'),
        ], heading="Aside block"),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Dogear boxes"),
        MultiFieldPanel([
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
        ], heading="Individual Volunteer Opportunity constants"),
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
