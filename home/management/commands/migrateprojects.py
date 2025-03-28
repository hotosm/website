from datetime import date
import json
from io import BytesIO
import os
import marko
import frontmatter
from django.db import transaction

from django.core.management.base import BaseCommand, CommandError
from app.projects.models import IndividualProjectPage, ProjectOwnerPage
from app.members.models import IndividualMemberPage, MemberOwnerPage, MemberGroupPage
from wagtail.fields import RichTextField, StreamField, StreamValue
from app.news.models import IndividualNewsPage, NewsOwnerPage, NewsCategory, NewsTag
from app.tech.models import IndividualTechStackPage
from app.core.models import Partner
from app.mapping_hubs.models import IndividualMappingHubPage
from app.impact_areas.models import IndividualImpactAreaPage
from modelcluster.contrib.taggit import ClusterTaggableManager
from home.models import HomePage
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from home.management.migration_helpers import create_image_from_url, convert_markdown_contents, comb_keys


FRONTMATTER_FIELD_TO_PROJECT_FIELD_DICT = {
    "Project Summary Text": ("intro", lambda intro: f"<p>{intro}</p>"),
    "Feature Image": ('header_image', lambda link: create_image_from_url(link, link)),
    "Impact Area": ('impact_area_list', lambda areas: get_impact_areas(areas)),
    "Country": ('country_text', lambda countries: get_countries(countries)),
    "Is Community-Led": ('is_community_led', lambda comled: comled),
    "People": ('project_contributors', lambda people: get_contributors(people)),
    "Partner": ('partner_list', lambda partners: get_partners(partners)),
    "Tools": ('tools_list', lambda tools: get_tools(tools)),
    "Data": ('data_links', lambda data: get_data(data)),
}


IMPACT_AREA_SEARCH_MAPPING_DICT = {
    'Gender Equality': 'Gender Equality', 

    'Sustainable Cities & Communities': 'Climate Resilience & Sustainability', 
    'Sustainable Cities and Communities': 'Climate Resilience & Sustainability', 
    'Clean Energy': 'Climate Resilience & Sustainability', 
    'Sustainable Cities': 'Climate Resilience & Sustainability', 

    'Public Health': 'Public Health', 

    'Disaster Response': 'Disaster Response', 
    'Disasters & Climate Resilience': 'Disaster Response', 

    'Refugee Response': 'Displacement & Safe Migration', 
    'Displacement & Safe Migration': 'Displacement & Safe Migration',
}

TECH_STACK_MAPPING_DICT = {
    'Tasking Manager': 'Tasking Manager',
    'Export Tool': 'HOT Export Tool',
    'HOT Export Tool': 'HOT Export Tool',
    'OpenAerialMap': 'Open Aerial Map (OAM)',
    'FMTM': 'Field Mapping Tasking Manager (FMTM)',
    'Field Mapping Tasking Manager': 'Field Mapping Tasking Manager (FMTM)',
}


def get_data(data):
    data_list = []

    for datum in data:
        if 'title' not in datum.keys() or 'link' not in datum.keys():
            continue
        data_list += [{'type': 'data', 'value': {'text': datum['title'], 'link': datum['link']}}]
    
    return data_list


def get_individual_tool(tool):
    if tool['tool'] in TECH_STACK_MAPPING_DICT.keys():
        results = IndividualTechStackPage.objects.live().search(TECH_STACK_MAPPING_DICT[tool['tool']])
        page = results.get_queryset()[0].get_translation(1)
        return {'type': 'tool', 'value': page.id}
    
    manual_tool_val = {'text': tool['tool']}
    if 'link' in tool.keys():
        manual_tool_val['link'] = tool['link']
    
    return {'type': 'manual_tool', 'value': manual_tool_val}


def get_tools(tools):
    stack = []

    for tool in tools:
        if 'tool' not in tool.keys() or isinstance(tool['tool'], list):
            continue
        stack += [get_individual_tool(tool)]

    return stack


def get_individual_partner(partner: str):
    results = Partner.objects.filter(partner_name=partner)
    
    if not results:
        return {"type": "manual_partner", "value": partner}
    
    return {"type": "partner", "value": results[0].pk}


def get_partners(partners):
    partner_list = []

    if isinstance(partners, list):
        # some random pages for some reason are like [[partner 1, partner 2]] so this is for that
        if isinstance(partners[0], list):
            partners = partners[0]

        for partner in partners:
            partner_list += [get_individual_partner(partner)]
    else:
        partner_list += [get_individual_partner(partners)]

    return partner_list


def get_individual_contributor(person):
    contributor = {}

    results = IndividualMemberPage.objects.live().search(person).get_queryset()
    if results:
        contributor['type'] = 'contributor'
        contributor['value'] = results[0].get_translation(1).id
    else:
        contributor['type'] = 'manual_contributor'
        contributor['value'] = person

    return contributor


def get_contributors(people):
    if not people:
        return []
    
    contributors = []
    if isinstance(people, list):
        # some random pages for some reason are like [[person 1, person 2]] so this is for that
        if isinstance(people[0], list):
            people = people[0]
        
        for person in people:
            if person:
                contributors += [get_individual_contributor(person)]
    else:
        contributors += [get_individual_contributor(people)]
    
    return contributors


def get_countries(countries):
    countries_str = ""
    for country in countries:
        countries_str += f"<p>{country}</p>"
    
    return countries_str


def get_duration_dates(article: frontmatter.Post, project_dict: dict):
    if 'Duration' not in article.keys():
        return
    
    duration = article['Duration']

    if 'Start Date' in duration.keys():
        project_dict['duration_start'] = duration['Start Date']
    if 'End Date' in duration.keys() and not isinstance(duration['End Date'], str):
        project_dict['duration_end'] = duration['End Date']


def get_impact_areas(areas):
    streamfield_areas = []
    areas_set = set()

    for area in areas:
        if area in IMPACT_AREA_SEARCH_MAPPING_DICT.keys():
            query = IMPACT_AREA_SEARCH_MAPPING_DICT[area]
            page = IndividualImpactAreaPage.objects.live().search(query).get_queryset()[0].get_translation(1)
            areas_set.add(page.id)
    
    for area in areas_set:
        streamfield_areas += [{'type': 'impact_area', 'value': area}]
    
    return streamfield_areas


def markdown_article_to_project_dict(article: frontmatter.Post):
    project_dict = {
        "title": article['title'],
        'description': convert_markdown_contents(article.content),
    }

    for key in FRONTMATTER_FIELD_TO_PROJECT_FIELD_DICT.keys():
        if key in article.keys():
            field, func = FRONTMATTER_FIELD_TO_PROJECT_FIELD_DICT[key]
            project_dict[field] = func(article[key])

    return project_dict


def create_project_page_from_markdown(file):
    article = frontmatter.load(file)
    if not 'title' in article.keys():
        return
    
    project_dict = markdown_article_to_project_dict(article)
    get_duration_dates(article, project_dict)
    
    page = IndividualProjectPage(**project_dict)
    owner = ProjectOwnerPage.objects.all()[0].get_translation(1)
    owner.add_child(instance=page)
    revision = page.save_revision()
    if 'published' in article.keys() and not article['published']:
        page.unpublish()
        return
    revision.publish()


def convert_all_projects_in_dir(directory):
    for filename in os.listdir(directory):
        if not filename.endswith('.markdown') and not filename.endswith('.md'):
            continue
        with open(f"{directory}/{filename}", 'r') as file:
            create_project_page_from_markdown(file)
            print('Converted:', filename)


def remigrate_project_images(file):
    article = frontmatter.load(file)
    if not 'title' in article.keys() or not 'Feature Image' in article.keys() or ('Feature Image' in article.keys() and not article['Feature Image'].startswith("https://cdn.hotosm.org")):
        return
    
    project = IndividualProjectPage.objects.all().filter(title=article['title'])[0].get_translation(1)

    if project.image:
        return

    image = create_image_from_url(article['Feature Image'], article['Feature Image'])

    project.image = image

    with transaction.atomic():
        project.save()
    
    print("Remigrated:", article['title'])


def remigrate_project_images_in_dir(directory):
    for filename in os.listdir(directory):
        if not filename.endswith('.markdown') and not filename.endswith('.md'):
            continue
        with open(f"{directory}/{filename}", 'r') as file:
            remigrate_project_images(file)


def test_markdown_conversion():
    path = "migration_pages/projects/dar-ramani-huria-dar-open-map.md"
    # filename = "2025-02-18-rutas-para-el-desarrollo-mapeando-caminos-para-la-conectividad-y-el-desarrollo-en-guatemala.markdown"
    with open(path, 'r') as file:
        create_project_page_from_markdown(file)
        # article = frontmatter.load(file)
        # print(article['People'])


class Command(BaseCommand):
    help = "Migrates projects"

    def handle(self, *args, **options):
        self.stdout.write("i'm testing! i'm testing!")
        # convert_all_projects_in_dir("migration_pages/projects")
        # remigrate_project_images_in_dir("migration_pages/_projects")
