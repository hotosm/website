from django import forms
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
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


class IndividualProgramPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        projects = IndividualProjectPage.objects.filter(owner_program=context['page'])
        context['projects'] = projects
        return context

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

    stats_title = models.CharField(default="Stats")
    stats = StreamField(ProgramStatBlock(), use_json_field=True, null=True, blank=True)

    goals_title = models.CharField(default="Goals")
    goals = StreamField(ProgramGoalBlock(), use_json_field=True, null=True, blank=True)

    projects_title = models.CharField(default="Projects")

    partners_title = models.CharField(default="Meet Our Partners")
    view_all_partners_title = models.CharField(default="View All Partners")
    view_all_partners_link = models.CharField(blank=True)
    partners = ParentalManyToManyField('core.Partner', blank=True)

    more_programs_title = models.CharField(default="More Programs")
    view_all_programs_title = models.CharField(default="View All Programs")
    view_all_programs_link = models.URLField(blank=True)
    more_programs = StreamField([
        ('program_page', PageChooserBlock(page_type="programs.IndividualProgramPage"))
    ], use_json_field=True, null=True, blank=True)

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
            FieldPanel("stats_title"),
            FieldPanel("stats"),
        ], heading="Stats"),
        MultiFieldPanel([
            FieldPanel("goals_title"),
            FieldPanel("goals"),
        ], heading="Goals"),
        MultiFieldPanel([
            FieldPanel("projects_title"),
        ], heading="Projects"),
        MultiFieldPanel([
            FieldPanel("partners_title"),
            FieldPanel("view_all_partners_title"),
            FieldPanel("view_all_partners_link"),
            FieldPanel("partners", widget=forms.CheckboxSelectMultiple),
        ], heading="Partners"),
        MultiFieldPanel([
            FieldPanel("more_programs_title"),
            FieldPanel("view_all_programs_title"),
            FieldPanel("view_all_programs_link"),
            FieldPanel("more_programs"),
        ], heading="Programs")
    ]
