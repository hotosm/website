from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.search import index
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from app.projects.models import IndividualProjectPage
from app.core.models import LinkOrPageBlock, Partner


class IndividualStatBlock(StructBlock):
    title = CharBlock()
    description = CharBlock()


class ProgramStatBlock(StreamBlock):
    stat_block = IndividualStatBlock()


class IndividualGoalBlock(StructBlock):
    title = CharBlock()
    description = RichTextBlock()
    icon = ImageChooserBlock()


class ProgramGoalBlock(StreamBlock):
    goal_block = IndividualGoalBlock()


class ProgramOwnerPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        base_locale = context['page'].get_translation(1).locale

        keyword = request.GET.get('keyword', '')
        programs = IndividualProgramPage.objects.live().filter(locale=base_locale)
        
        if keyword:
            programs = programs.search(keyword).get_queryset()

        match request.GET.get('sort', ''):
            case 'sort.new':
                programs = programs.order_by('-program_start_date')
            case 'sort.old':
                programs = programs.order_by('program_start_date')
            case 'sort.titlea':
                programs = programs.order_by('title')
            case 'sort.titlez':
                programs = programs.order_by('-title')
            case _:
                programs = programs.order_by('-program_start_date')
        
        context['programs'] = programs
        return context

    max_count = 1

    subpage_types = [
        'programs.IndividualProgramPage'
    ]

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    keyword_search_hint = models.CharField(default="Search by keyword")
    sort_by_new = models.CharField(default="Sort by New")
    sort_by_old = models.CharField(default="Sort by Old")
    sort_by_titlea = models.CharField(default="Sort by Title Alphabetical")
    sort_by_titlez = models.CharField(default="Sort by Title Reverse Alphabetical")
    search_button_text = models.CharField(default="Apply Filters")
    remove_filters_text = models.CharField(default="Reset Filters")

    red_box_title = models.CharField(default="See all of HOT’s projects")
    red_box_link_text = models.CharField(default="Explore projects")
    red_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="See the many ways to get involved with HOT and open mapping")
    black_box_link_text = models.CharField(default="Get involved")
    black_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    # v individual program page stuff v
    stats_title = models.CharField(default="Stats")
    goals_title = models.CharField(default="Goals")
    projects_title = models.CharField(default="Projects")

    partners_title = models.CharField(default="Meet Our Partners")
    view_all_partners_title = models.CharField(default="View All Partners")
    view_all_partners_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    more_programs_title = models.CharField(default="More Programs")
    view_all_programs_title = models.CharField(default="View All Programs")
    view_all_programs_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    bottom_banner_text = models.CharField(default="Check out the many opportunities to get involved with HOT!")
    bottom_banner_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    bottom_banner_url_text = models.CharField(default="Get Involved with HOT")

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        MultiFieldPanel([
            FieldPanel('keyword_search_hint'),
            FieldPanel('sort_by_new'),
            FieldPanel('sort_by_old'),
            FieldPanel('sort_by_titlea'),
            FieldPanel('sort_by_titlez'),
            FieldPanel('search_button_text'),
            FieldPanel('remove_filters_text'),
        ], heading="Filtering"),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Dogear Boxes"),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel("stats_title"),
                FieldPanel("goals_title"),
                FieldPanel("projects_title"),
            ], heading="Various Section Titles"),
            MultiFieldPanel([
                FieldPanel("partners_title"),
                FieldPanel("view_all_partners_title"),
                FieldPanel("view_all_partners_link_url"),
            ], heading="Partners"),
            MultiFieldPanel([
                FieldPanel("more_programs_title"),
                FieldPanel("view_all_programs_title"),
                FieldPanel("view_all_programs_link_url"),
            ], heading="Programs"),
            MultiFieldPanel([
                FieldPanel('bottom_banner_text'),
                FieldPanel('bottom_banner_link_url'),
                FieldPanel('bottom_banner_url_text'),
            ]),
        ], heading="Individual Program Page Shared Fields"),
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

    partner_list = StreamField([('partner', SnippetChooserBlock(Partner))], use_json_field=True, null=True, blank=True)

    more_programs = StreamField([
        ('program_page', PageChooserBlock(page_type="programs.IndividualProgramPage"))
    ], use_json_field=True, null=True, blank=True)

    program_start_date = models.DateField(help_text="This is not shown on the program page itself, and is basically just used for sorting on the program owner page.")

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
            FieldPanel("partner_list"),
        ], heading="Partners"),
        MultiFieldPanel([
            FieldPanel("more_programs"),
        ], heading="Programs"),
        MultiFieldPanel([
            FieldPanel('program_start_date'),
        ], heading="Others"),
    ]
