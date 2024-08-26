import re

from django import forms
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from app.projects.models import IndividualProjectPage, ProjectType, ProjectStatus
from app.impact_areas.models import IndividualImpactAreaPage
from app.mapping_hubs.models import MappingHubProjectsPage, IndividualMappingHubPage
from app.programs.models import IndividualProgramPage
from app.core.models import LinkOrPageBlock


class OurWorkPage(Page):
    def get_project_paginator(self, request, context):
        projects_list = IndividualProjectPage.objects.live().filter(locale=context['page'].locale)

        keyword = request.GET.get('keyword', '')

        if keyword:
            projects_list = projects_list.search(keyword).get_queryset()
        
        p_types = ProjectType.objects.all()
        query = Q()
        for p_type in p_types:
            if request.GET.get(str(p_type), ''):
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
        
        hubs = IndividualMappingHubPage.objects.live().filter(locale=context['page'].locale)
        query = Q()
        for hub in hubs:
            if request.GET.get(f"hub{hub.id}", ''):
                query = query | Q(region_hub_list__contains=[{'type': 'region_hub', 'value': hub.id }])
        projects_list = projects_list.filter(query).distinct()
        
        impact_areas = IndividualImpactAreaPage.objects.live().filter(locale=context['page'].locale)
        query = Q()
        for area in impact_areas:
            if request.GET.get(f"ia{area.id}", ''):
                query = query | Q(impact_area_list__contains=[{'type': 'impact_area', 'value': area.id }])
        projects_list = projects_list.filter(query).distinct()

        programs = IndividualProgramPage.objects.live().filter(locale=context['page'].locale)
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
        
        return paginator, projects

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        paginator, projects = self.get_project_paginator(request, context)
        
        context['projects'] = projects
        context['paginator'] = paginator
        context['impact_areas'] = IndividualImpactAreaPage.objects.live().filter(locale=context['page'].locale)
        context['hubs'] = IndividualMappingHubPage.objects.live().filter(locale=context['page'].locale)
        context['hubs_projects'] = MappingHubProjectsPage.objects.live().filter(locale=context['page'].locale)
        context['programs'] = IndividualProgramPage.objects.live().filter(locale=context['page'].locale)
        context['types'] = ProjectType.objects.all()
        context['statuses'] = ProjectStatus.objects.all()
        return context
    
    def serve(self, request, *args, **kwargs):
        if request.GET.get('projects', False):
            context = super().get_context(request, *args, **kwargs)
            _, projects = self.get_project_paginator(request, context)

            features = []
            for project in projects:
                if not project.location_coordinates:
                    continue
                coordinates = [float(x) for x in re.findall("\(([^\)]+)\)", project.location_coordinates)[0].split()]
                features += [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": coordinates
                        },
                        "properties": {
                            "title": f"{project.title}",
                            "description": f"{project.intro}",
                            "id": f"{project.id}",
                        }
                    }
                ]

            geojson = {
                "type": "FeatureCollection",
                "features": features,
            }

            return JsonResponse(geojson)
            
        return super().serve(request, *args, **kwargs)

    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image",
    )

    programs_title = models.CharField(default="Highlighted Programs")
    programs_description = RichTextField(blank=True)
    view_all_programs_text = models.CharField(default="View all programs")
    view_all_programs_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    highlighted_programs = StreamField([('program', PageChooserBlock(page_type="programs.IndividualProgramPage"))], use_json_field=True, null=True, blank=True)

    projects_title = models.CharField(default="Projects")
    search_keyword_text = models.CharField(default="Search by keyword")
    sort_new_text = models.CharField(default="Sort by New")
    sort_old_text = models.CharField(default="Sort by Old")
    sort_titlea_text = models.CharField(default="Sort by Name Alphabetical")
    sort_titlez_text = models.CharField(default="Sort by Name Reverse Alphabetical")
    filters_text = models.CharField(default="Filters")
    view_grid_text = models.CharField(default="View Grid")
    view_map_text = models.CharField(default="View Map")

    f_impact_areas_text = models.CharField(default="Impact Areas")
    f_open_mapping_hubs_text = models.CharField(default="Open Mapping Hubs")
    f_projects_by_programme_text = models.CharField(default="Projects by Programme")
    f_projects_by_type_text = models.CharField(default="Projects by Type")
    f_project_status_text = models.CharField(default="Project Status")
    f_apply_filter_text = models.CharField(default="Apply Filter")
    f_reset_filters_text = models.CharField(default="Reset Filters")

    load_more_projects_text = models.CharField(default="Load More Projects")
    no_projects_found = models.CharField(default="No projects found with the applied filters.")
    impact_area_title = models.CharField(default="See Projects by Impact Area")
    open_mapping_hub_title = models.CharField(default="See Projects by Open Mapping Hub")

    red_box_title = models.CharField(default="Check our upcoming events!")
    red_box_link_text = models.CharField(default="View all events")
    red_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="Check many opportunities to get involved with HOT!")
    black_box_link_text = models.CharField(default="Get Involved with HOT")
    black_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        MultiFieldPanel([
            FieldPanel('programs_title'),
            FieldPanel('programs_description'),
            FieldPanel('view_all_programs_text'),
            FieldPanel('view_all_programs_link'),
            FieldPanel('highlighted_programs'),
        ], heading="Programs"),
        MultiFieldPanel([
            FieldPanel('projects_title'),
            FieldPanel('search_keyword_text'),
            FieldPanel('sort_new_text'),
            FieldPanel('sort_old_text'),
            FieldPanel('sort_titlea_text'),
            FieldPanel('sort_titlez_text'),
            FieldPanel('filters_text'),
            FieldPanel('view_grid_text'),
            FieldPanel('view_map_text'),
            MultiFieldPanel([
                FieldPanel('f_impact_areas_text'),
                FieldPanel('f_open_mapping_hubs_text'),
                FieldPanel('f_projects_by_programme_text'),
                FieldPanel('f_projects_by_type_text'),
                FieldPanel('f_project_status_text'),
                FieldPanel('f_apply_filter_text'),
                FieldPanel('f_reset_filters_text'),
            ], heading="Filters Menu"),
            FieldPanel('load_more_projects_text'),
            FieldPanel('no_projects_found'),
        ], heading="Projects Section"),
        MultiFieldPanel([
            FieldPanel('impact_area_title'),
            FieldPanel('open_mapping_hub_title'),
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link'),
        ], heading="Bottom Area"),
    ]
