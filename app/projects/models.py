from django import forms
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.search import index
from wagtail.snippets.models import register_snippet

from wagtailgeowidget.panels import LeafletPanel

from modelcluster.fields import ParentalKey, ParentalManyToManyField

from app.core.models import LinkOrPageBlock, Partner
import importlib
# from app.impact_areas.models import IndividualImpactAreaPage
# from app.mapping_hubs.models import MappingHubProjectsPage, IndividualMappingHubPage
# from app.programs.models import IndividualProgramPage


"""
This page should only be created as a child of an IndividualMappingHubPage!
Its template depends on fields from the IndividualMappingHubPage in order
to create one unifying place where unchanging fields may be modified.
"""
class ProjectOwnerPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        ia_module = importlib.import_module("app.impact_areas.models")
        IndividualImpactAreaPage = getattr(ia_module, "IndividualImpactAreaPage")
        hub_module = importlib.import_module("app.mapping_hubs.models")
        IndividualMappingHubPage = getattr(hub_module, "IndividualMappingHubPage")
        pr_module = importlib.import_module("app.programs.models")
        IndividualProgramPage = getattr(pr_module, "IndividualProgramPage")

        projects_list = IndividualProjectPage.objects.live().filter(locale=context['page'].locale)

        keyword = request.GET.get('keyword', '')

        if keyword:
            projects_list = projects_list.search(keyword).get_queryset()
        
        p_types = ProjectType.objects.all()
        query = Q()
        for p_type in p_types:
            if request.GET.get("pt" + str(p_type.id), ''):
                query = query | Q(types=p_type)
        projects_list = projects_list.filter(query).distinct()

        if request.GET.get("status", 'statusnone') != "statusnone":
            statuses = ProjectStatus.objects.all()
            query = Q()
            for status in statuses:
                if request.GET.get("status", '') == f"status{status.id}":
                    query = query | Q(project_status=status)
                    break
            projects_list = projects_list.filter(query).distinct()
        
        base_locale = context['page'].get_translation(1).locale
        
        hubs = IndividualMappingHubPage.objects.live().filter(locale=base_locale)
        query = Q()
        for hub in hubs:
            if request.GET.get(f"hub{hub.id}", ''):
                query = query | Q(region_hub_list__contains=[{'type': 'region_hub', 'value': hub.id }])
        projects_list = projects_list.filter(query).distinct()
        
        impact_areas = IndividualImpactAreaPage.objects.live().filter(locale=base_locale)
        query = Q()
        for area in impact_areas:
            if request.GET.get(f"ia{area.id}", ''):
                query = query | Q(impact_area_list__contains=[{'type': 'impact_area', 'value': area.id }])
        projects_list = projects_list.filter(query).distinct()

        programs = IndividualProgramPage.objects.live().filter(locale=base_locale)
        query = Q()
        for program in programs:
            if request.GET.get(f"pg{program.id}", ''):
                query = query | Q(owner_program=program)
        projects_list = projects_list.filter(query).distinct()

        match request.GET.get('sort', ''):
            case 'sort.titlea':
                projects_list = projects_list.order_by('title')
            case 'sort.titlez':
                projects_list = projects_list.order_by('-title')
            case _:
                projects_list = projects_list.order_by('title')

        page = request.GET.get('page', 1)
        paginator = Paginator(projects_list, 8)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)

        context['projects'] = projects
        context['paginator'] = paginator
        context['impact_areas'] = impact_areas
        context['hubs'] = hubs
        context['programs'] = programs
        context['types'] = ProjectType.objects.all()
        context['statuses'] = ProjectStatus.objects.all()
        context['current_page'] = int(page)
        return context
    
    max_count = 1

    subpage_types = [
        'projects.IndividualProjectPage'
    ]

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    search_keyword_text = models.CharField(default="Search by keyword")
    sort_titlea_text = models.CharField(default="Sort by Name Alphabetical")
    sort_titlez_text = models.CharField(default="Sort by Name Reverse Alphabetical")
    impact_areas_text = models.CharField(default="Filter by Impact Area")
    open_mapping_hubs_text = models.CharField(default="Filter by Hub")
    projects_by_programme_text = models.CharField(default="Filter by Program")
    projects_by_type_text = models.CharField(default="Filter by Type")
    project_status_text = models.CharField(default="Filter by Status")
    apply_filter_text = models.CharField(default="Apply Filter")
    reset_filters_text = models.CharField(default="Reset Filters")
    applied_text = models.CharField(default="applied")
    
    results_text = models.CharField(default="Results")
    load_more_projects_text = models.CharField(default="Load More Projects")

    bottom_dogear_title = models.CharField(default="See our projects on the map")
    bottom_dogear_link_text = models.CharField(default="Check our work")
    bottom_dogear_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    impact_areas_title = models.CharField(default="Impact Areas")
    region_hub_title = models.CharField(default="Region Hub/Country")
    duration_title = models.CharField(default="Duration")
    partners_title = models.CharField(default="Partners")
    tools_title = models.CharField(default="Tools")
    types_title = models.CharField(default="Project Type")
    contact_title = models.CharField(default="Contact")

    related_news_title = models.CharField(default="Related News")
    view_all_news_text = models.CharField(default="View all News")
    view_all_news_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    related_events_title = models.CharField(default="Related Events")
    view_all_events_text = models.CharField(default="View all Events")
    view_all_events_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    red_box_title = models.CharField(default="Chat with Our Community")
    red_box_link_text = models.CharField(default="Get connected now")
    red_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="Our Work")
    black_box_link_text = models.CharField(default="View Our Work")
    black_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            MultiFieldPanel([
                FieldPanel('search_keyword_text'),
                FieldPanel('sort_titlea_text'),
                FieldPanel('sort_titlez_text'),
                FieldPanel('impact_areas_text'),
                FieldPanel('open_mapping_hubs_text'),
                FieldPanel('projects_by_programme_text'),
                FieldPanel('projects_by_type_text'),
                FieldPanel('project_status_text'),
                FieldPanel('apply_filter_text'),
                FieldPanel('reset_filters_text'),
                FieldPanel('applied_text'),
            ], heading="Filters"),
            FieldPanel('results_text'),
            FieldPanel('load_more_projects_text'),
            FieldPanel('bottom_dogear_title'),
            FieldPanel('bottom_dogear_link_text'),
            FieldPanel('bottom_dogear_link'),
        ], heading="Project Page"),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('impact_areas_title'),
                FieldPanel('region_hub_title'),
                FieldPanel('duration_title'),
                FieldPanel('partners_title'),
                FieldPanel('tools_title'),
                FieldPanel('types_title'),
                FieldPanel('contact_title'),
                MultiFieldPanel([
                    FieldPanel('related_news_title'),
                    FieldPanel('view_all_news_text'),
                    FieldPanel('view_all_news_link'),
                    FieldPanel('related_events_title'),
                    FieldPanel('view_all_events_text'),
                    FieldPanel('view_all_events_link'),
                ], heading="Related Pages"),
            ], heading="Sidebar"),
            MultiFieldPanel([
                FieldPanel('red_box_title'),
                FieldPanel('red_box_link_text'),
                FieldPanel('red_box_link'),
                FieldPanel('black_box_title'),
                FieldPanel('black_box_link_text'),
                FieldPanel('black_box_link'),
            ], heading="Footer"),
        ], heading="Individual Project Page"),
    ]


@register_snippet
class ProjectType(models.Model):
    type_name = models.CharField()

    panels = [
        FieldPanel("type_name")
    ]

    def __str__(self):
        return self.type_name
    
    class Meta:
        verbose_name_plural = "Project Types"


@register_snippet
class ProjectStatus(models.Model):
    status_name = models.CharField()

    panels = [
        FieldPanel("status_name")
    ]

    def __str__(self):
        return self.status_name
    
    class Meta:
        verbose_name_plural = "Project Statuses"


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
        'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ]))
    ], use_json_field=True, null=True)

    call_to_action_title = models.CharField(default="Call to Action")
    call_to_action_description = RichTextField(null=True, blank=True)
    call_to_action_link_text = models.CharField(default="Call to Action Link")
    call_to_action_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    # > SIDE BAR
    project_status = models.ForeignKey(
        "projects.ProjectStatus",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    impact_area_list = StreamField([('impact_area', PageChooserBlock(page_type="impact_areas.IndividualImpactAreaPage"))], use_json_field=True, null=True, blank=True)
    region_hub_list = StreamField([('region_hub', PageChooserBlock(page_type="mapping_hubs.IndividualMappingHubPage"))], use_json_field=True, null=True, blank=True)
    country_text = RichTextField(blank=True, help_text="This field is not required; this field is mostly for projects with no specified region hub. Regardless, if region hub(s) and country are both provided, both fields will appear on the page.")
    duration = models.CharField(default="Ongoing", blank=True)
    partner_list = StreamField([('partner', SnippetChooserBlock(Partner))], use_json_field=True, null=True, blank=True)
    tools_list = StreamField([('tool', PageChooserBlock(page_type="tech.IndividualTechStackPage"))], use_json_field=True, null=True, blank=True)
    contact = RichTextField(null=True, blank=True, help_text="If you provide an email here, make sure to turn it into an email link. This can be done by highlighting the text containing the email and pressing CTRL + K.")
    types = ParentalManyToManyField('projects.ProjectType', blank=True)
    related_news = StreamField([
        ('news_page', PageChooserBlock(page_type="news.IndividualNewsPage"))
    ], use_json_field=True, null=True, blank=True)
    related_events = StreamField([
        ('event_page', PageChooserBlock(page_type="events.IndividualEventPage"))
    ], use_json_field=True, null=True, blank=True)

    project_contributors = StreamField([('contributor', PageChooserBlock(page_type="members.IndividualMemberPage"))], use_json_field=True, null=True, blank=True, help_text="If a member is listed as a contributor to a project, that project will appear on the given member's page.")
    location_coordinates = models.CharField(max_length=250, blank=True, null=True, help_text="Used to show where on the map the project takes place; used on the Our Work page.")

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('search_description'),
        index.SearchField('intro'),
    ]

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
                FieldPanel('call_to_action_link'),
            ], heading="Call to Action"),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('project_status', widget=forms.RadioSelect),
            FieldPanel('impact_area_list'),
            FieldPanel('region_hub_list'),
            FieldPanel('country_text'),
            FieldPanel('duration'),
            FieldPanel('partner_list'),
            FieldPanel('tools_list'),
            FieldPanel('contact'),
            FieldPanel('types', widget=forms.CheckboxSelectMultiple),
            MultiFieldPanel([
                FieldPanel('related_news'),
                FieldPanel('related_events'),
            ], heading="Related Pages"),
        ], heading="Sidebar"),
        MultiFieldPanel([
            FieldPanel('project_contributors'),
            LeafletPanel('location_coordinates'),
        ], heading="Extras")
    ]