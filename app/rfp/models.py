from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.models import Page


class RequestForProposalOwnerPage(Page):
    subpage_types = [
        'rfp.IndividualRequestForProposalPage'
    ]

    max_count = 1

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
    ]


class IndividualRequestForProposalPage(Page):
    parent_page_type = [
        'rfp.RequestForProposalOwnerPage'
    ]

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
