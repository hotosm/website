from django import forms
from django.db import models
from django.core.exceptions import ValidationError

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.search import index

from app.projects.models import IndividualProjectPage

from modelcluster.fields import ParentalKey, ParentalManyToManyField


class IndividualStatBlock(StructBlock):
    title = CharBlock()
    description = RichTextBlock()


class ProgramStatBlock(StreamBlock):
    stat_block = IndividualStatBlock()


class IndividualGoalBlock(StructBlock):
    title = CharBlock()
    description = RichTextBlock()
    icon = ImageChooserBlock()


class ProgramGoalBlock(StreamBlock):
    goal_block = IndividualGoalBlock()


class ProgramOwnerPage(Page):
    max_count = 1

    subpage_types = [
        'programs.IndividualProgramPage'
    ]
    
    stats_title = models.CharField(default="Stats")
    goals_title = models.CharField(default="Goals")
    projects_title = models.CharField(default="Projects")

    partners_title = models.CharField(default="Meet Our Partners")
    view_all_partners_title = models.CharField(default="View All Partners")
    view_all_partners_link = models.CharField(blank=True)

    more_programs_title = models.CharField(default="More Programs")
    view_all_programs_title = models.CharField(default="View All Programs")
    view_all_programs_link = models.URLField(blank=True)

    bottom_banner_text = models.CharField(default="Check out the many opportunities to get involved with HOT!")
    bottom_banner_url = models.URLField(blank=True)
    bottom_banner_url_text = models.CharField(default="Get Involved with HOT")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("stats_title"),
            FieldPanel("goals_title"),
            FieldPanel("projects_title"),
        ], heading="Various Section Titles"),
        MultiFieldPanel([
            FieldPanel("partners_title"),
            FieldPanel("view_all_partners_title"),
            FieldPanel("view_all_partners_link"),
        ], heading="Partners"),
        MultiFieldPanel([
            FieldPanel("more_programs_title"),
            FieldPanel("view_all_programs_title"),
            FieldPanel("view_all_programs_link"),
        ], heading="Programs"),
        MultiFieldPanel([
            FieldPanel('bottom_banner_text'),
            FieldPanel('bottom_banner_url'),
            FieldPanel('bottom_banner_url_text'),
        ]),
    ]


class IndividualProgramPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        projects = IndividualProjectPage.objects.filter(owner_program=context['page'], locale=context['page'].locale)
        context['projects'] = projects
        return context

    parent_page_type = [
        'programs.ProgramOwnerPage'
    ]

    subtitle = RichTextField(blank=True)
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Intro image"
    )

    stats = StreamField(ProgramStatBlock(), use_json_field=True, null=True, blank=True)

    goals = StreamField(ProgramGoalBlock(), use_json_field=True, null=True, blank=True)

    partners = ParentalManyToManyField('core.Partner', blank=True)

    more_programs = StreamField([
        ('program_page', PageChooserBlock(page_type="programs.IndividualProgramPage"))
    ], use_json_field=True, null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('search_description'),
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("subtitle"),
            FieldPanel("header_image"),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel("intro"),
            FieldPanel("description"),
            FieldPanel("intro_image"),
        ], heading="Intro"),
        MultiFieldPanel([
            FieldPanel("stats"),
        ], heading="Stats"),
        MultiFieldPanel([
            FieldPanel("goals"),
        ], heading="Goals"),
        MultiFieldPanel([
            FieldPanel("partners", widget=forms.CheckboxSelectMultiple),
        ], heading="Partners"),
        MultiFieldPanel([
            FieldPanel("more_programs"),
        ], heading="Programs"),
    ]
