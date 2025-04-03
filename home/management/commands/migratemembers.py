from datetime import date
import json
from io import BytesIO
import os
import marko
import frontmatter

from django.core.management.base import BaseCommand, CommandError
from app.projects.models import IndividualProjectPage
from app.members.models import IndividualMemberPage, MemberOwnerPage, MemberGroupPage
from wagtail.fields import RichTextField, StreamField, StreamValue
from app.news.models import IndividualNewsPage, NewsOwnerPage, NewsCategory, NewsTag
from app.mapping_hubs.models import IndividualMappingHubPage
from modelcluster.contrib.taggit import ClusterTaggableManager
from home.models import HomePage
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from home.management.migration_helpers import create_image_from_url, create_image_from_local_file, handle_markdown_images, convert_markdown_contents, HOTOSM_LEGACY_SITE_URL, comb_keys
from django.db import transaction


FRONTMATTER_FIELD_TO_MEMBER_FIELD_GUIDE = {
    "Member Type": ("member_groups", lambda groups: get_member_groups(groups)),
    "Photo": ("image", lambda link: create_image_from_url(link, link)),
    "Job Title": ("position", lambda pos: pos),
    "Country": ("country", lambda country: country),
    "Social Media (Full URL)": ("on_the_web_links", lambda links: get_socials_links(links)),
    "Team": ("location_hub", lambda team: get_hub(team)),
}


def test_markdown_conversion():
    path = "migration_pages/_people/arnalie-vicario.markdown"
    # filename = "2025-02-18-rutas-para-el-desarrollo-mapeando-caminos-para-la-conectividad-y-el-desarrollo-en-guatemala.markdown"
    with open(path, 'r') as file:
        create_member_page_from_markdown(file)


def test_random_garbage():
    result: IndividualMemberPage = IndividualMemberPage.objects.live().search("Meredith Grey").get_queryset()[0]
    links: StreamValue = result.on_the_web_links
    print(links.get_prep_value())


def get_hub(team):
    match team:
        case 'West and Northern Africa Hub':
            return IndividualMappingHubPage.objects.live().search("West & Northern Africa").get_queryset()[0].get_translation(1)
        case 'Asia Pacific Hub':
            return IndividualMappingHubPage.objects.live().search("Asia-Pacific").get_queryset()[0].get_translation(1)
        case 'Eastern and Southern Africa Hub':
            return IndividualMappingHubPage.objects.live().search("Eastern & Southern Africa").get_queryset()[0].get_translation(1)
        case 'Latin America and Caribbean Hub':
            return IndividualMappingHubPage.objects.live().search("Latin America and the Caribbean").get_queryset()[0].get_translation(1)
        case _:
            return None


def get_member_groups(groups):
    mem_groups = []

    keys = groups.keys()
    if 'Is Voting Member' in keys and groups['Is Voting Member']:
        page = MemberGroupPage.objects.live().search("Voting Members").get_queryset()[0].get_translation(1)
        mem_groups += [{'type': 'member_group', 'value': {
            'group': page.id,
            'role': 'Voting Member',
        }}]
    
    if 'Is Staff' in keys and groups['Is Staff']:
        page = MemberGroupPage.objects.live().search("Staff Members").get_queryset()[0].get_translation(1)
        mem_groups += [{'type': 'member_group', 'value': {
            'group': page.id,
            'role': 'Staff',
        }}]
    
    if 'Is Board Member' in keys and groups['Is Board Member']:
        page = MemberGroupPage.objects.live().search("Board Members").get_queryset()[0].get_translation(1)
        mem_groups += [{'type': 'member_group', 'value': {
            'group': page.id,
            'role': 'Board',
        }}]
    
    return mem_groups


def get_socials_links(article_links):
    socials_links = []
    
    for link in article_links.keys():
        socials_links += [{
            'type': 'blocks',
            'value': {
                'link_url': article_links[link],
                'link_text': link,
            }
        }]
    
    return socials_links


def markdown_article_to_member_dict(article: frontmatter.Post):
    body = article.content
    member_dict = {
        "title": article['title'],
        "body": json.dumps([{'type': 'md_block', 'value': body}]),
    }

    for key in FRONTMATTER_FIELD_TO_MEMBER_FIELD_GUIDE.keys():
        if key in article.keys():
            field, func = FRONTMATTER_FIELD_TO_MEMBER_FIELD_GUIDE[key]
            member_dict[field] = func(article[key])

    return member_dict


def create_member_page_from_markdown(file):
    article = frontmatter.load(file)
    if not 'title' in article.keys():
        return
    
    member_dict = markdown_article_to_member_dict(article)
    
    page = IndividualMemberPage(**member_dict)
    owner = MemberOwnerPage.objects.all()[0].get_translation(1)
    owner.add_child(instance=page)
    revision = page.save_revision()
    if 'published' in article.keys() and not article['published']:
        page.unpublish()
        return
    revision.publish()


def convert_all_members_in_dir(directory):
    for filename in os.listdir(directory):
        if not filename.endswith('.markdown') and not filename.endswith('.md'):
            continue
        with open(f"{directory}/{filename}", 'r') as file:
            create_member_page_from_markdown(file)
            print('Converted:', filename)


def add_projects_to_member(file):
    article = frontmatter.load(file)
    if not 'title' in article.keys() or not 'Project' in article.keys():
        return
    
    member = IndividualMemberPage.objects.all().filter(title=article['title'])[0].get_translation(1)
    
    for project in article['Project']:
        if not isinstance(project, str):
            continue

        results = IndividualProjectPage.objects.all().filter(title=project)

        if not results:
            continue

        proj_page = results[0].get_translation(1)

        contributors = [{'type': 'contributor', 'value': member.id}]
        for contributor in proj_page.project_contributors:
            contributors += [{'type': 'contributor', 'value': contributor.value.id}]

        proj_page.project_contributors = contributors

        with transaction.atomic():
            proj_page.save()
    
    print("Completed:", article['title'])


def add_projects_to_members_in_dir(directory):
    for filename in os.listdir(directory):
        if not filename.endswith('.markdown') and not filename.endswith('.md'):
            continue
        with open(f"{directory}/{filename}", 'r') as file:
            add_projects_to_member(file)


def verify_publish_status(file):
    article = frontmatter.load(file)
    if not 'title' in article.keys() or not 'published' in article.keys() or ('published' in article.keys() and article['published']):
        return
    
    member = IndividualMemberPage.objects.all().filter(title=article['title'])[0].get_translation(1)

    member.unpublish()

    with transaction.atomic():
        member.save()
    
    print("Unpublished:", article['title'])


# this was made because i forgot to check for published status in members
def verify_publish_status_in_dir(directory):
    for filename in os.listdir(directory):
        if not filename.endswith('.markdown') and not filename.endswith('.md'):
            continue
        with open(f"{directory}/{filename}", 'r') as file:
            verify_publish_status(file)


'''
# this function was temporary to change the format of the member's body text!
# you can ignore it, but it's staying here just in case...
def convert_member_intro_to_body():
    pages = IndividualMemberPage.objects.all().filter(locale=1)
    for page in pages:
        if not page.intro:
            continue
        page.body = [{'type': 'md_block', 'value': page.intro}]
        with transaction.atomic():
            page.save()'
'''


class Command(BaseCommand):
    help = "Migrates members"

    def handle(self, *args, **options):
        self.stdout.write("i'm testing! i'm testing!")
        convert_all_members_in_dir("migration_pages/members")
        add_projects_to_members_in_dir("migration_pages/members")
        # convert_member_intro_to_body()
        # add_projects_to_members_in_dir("migration_pages/_people")
        # add_projects_to_members_in_dir("migration_pages/_people/staff")
        # add_projects_to_members_in_dir("migration_pages/_people/voting-members")
        # verify_publish_status_in_dir("migration_pages/_people")
        # verify_publish_status_in_dir("migration_pages/_people/staff")
        # verify_publish_status_in_dir("migration_pages/_people/voting-members")
