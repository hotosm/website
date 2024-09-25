from django.db import models
from django.utils import timezone

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.models import Page

from app.core.models import LinkOrPageBlock


class RequestForProposalOwnerPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        rfps = IndividualRequestForProposalPage.objects.live().filter(locale=context['page'].locale)
        rfps = rfps.filter(application_close_date__gte=timezone.now().date(), is_active=True)
        
        context['rfps'] = rfps
        return context

    subpage_types = [
        'rfp.IndividualRequestForProposalPage'
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

    current_rfps_title = models.CharField(default="Current RFPs")
    rfp_location_text = models.CharField(default="Location")
    rfp_deadline_text = models.CharField(default="Deadline")
    no_rfps_title = models.CharField(default="There are no current RFPs.")
    no_rfps_description = RichTextField(blank=True)

    aside_block_title = models.CharField(default="Still have questions?")
    aside_block_description = RichTextField(blank=True)

    job_opportunities_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Job opportunities image"
    )
    job_opportunities_title = models.CharField(default="See Our Job Opportunities")
    job_opportunities_description = RichTextField(blank=True)
    job_opportunities_button_text = models.CharField(default="See All Job Opportunities")
    job_opportunities_button_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    posted_by_prefix_text = models.CharField(default="Posted by")

    terms_of_reference_title = models.CharField(default="Terms of Reference")
    role_title = models.CharField(default="Role:")
    application_close_title = models.CharField(default="Application Close Date:")
    project_duration_title = models.CharField(default="Duration of Project:")
    work_location_title = models.CharField(default="Work Location:")
    contract_type_title = models.CharField(default="Type of Contract:")
    direct_contact_title = models.CharField(default="Direct Contact:")
    cta_title = models.CharField(blank=True)
    submission_email_button = models.CharField(default="Submission Email")

    go_back_text = models.CharField(default="Go Back to Request for Proposals")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_description'),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('current_rfps_title'),
            FieldPanel('rfp_location_text'),
            FieldPanel('rfp_deadline_text'),
            FieldPanel('no_rfps_title'),
            FieldPanel('no_rfps_description'),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('aside_block_title'),
            FieldPanel('aside_block_description'),
        ], heading="Aside"),
        MultiFieldPanel([
            FieldPanel('job_opportunities_image'),
            FieldPanel('job_opportunities_title'),
            FieldPanel('job_opportunities_description'),
            FieldPanel('job_opportunities_button_text'),
            FieldPanel('job_opportunities_button_url'),
        ], heading="Footer banner"),
        MultiFieldPanel([
            FieldPanel('posted_by_prefix_text'),
            MultiFieldPanel([
                FieldPanel('terms_of_reference_title'),
                FieldPanel('role_title'),
                FieldPanel('application_close_title'),
                FieldPanel('project_duration_title'),
                FieldPanel('work_location_title'),
                FieldPanel('contract_type_title'),
                FieldPanel('direct_contact_title'),
                FieldPanel('cta_title'),
                FieldPanel('submission_email_button'),
            ], heading="Sidebar"),
            FieldPanel('go_back_text'),
        ], heading="Individual RFP Page"),
    ]


class IndividualRequestForProposalPage(Page):
    parent_page_type = [
        'rfp.RequestForProposalOwnerPage'
    ]

    is_active = models.BooleanField(default=True)

    posters = StreamField([('poster', PageChooserBlock(page_type="members.IndividualMemberPage"))], use_json_field=True, null=True, blank=True)
    post_date = models.DateField(blank=True, null=True)

    intro = RichTextField(blank=True)
    article_body = StreamField([
        ('text_block', RichTextBlock(features=[
        'h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ]))
    ], use_json_field=True, null=True, blank=True)

    role = models.CharField(blank=True)
    application_close_date = models.DateField(blank=True, null=True)
    project_duration = models.CharField(blank=True)
    work_location = models.CharField(blank=True)
    contract_type = models.CharField(blank=True)
    direct_contact = models.CharField(blank=True)
    submission_email = models.EmailField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('is_active'),
        FieldPanel('posters'),
        FieldPanel('post_date'),
        FieldPanel('intro'),
        FieldPanel('article_body'),
        MultiFieldPanel([
            FieldPanel('role'),
            FieldPanel('application_close_date'),
            FieldPanel('project_duration'),
            FieldPanel('work_location'),
            FieldPanel('contract_type'),
            FieldPanel('direct_contact'),
            FieldPanel('submission_email'),
        ], heading="Sidebar"),
    ]
