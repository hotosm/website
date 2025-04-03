from datetime import date
import json
from io import BytesIO
import os
import marko
import frontmatter
from django.db import transaction

from django.core.management.base import BaseCommand, CommandError
from app.news.models import IndividualNewsPage, NewsOwnerPage, NewsCategory, NewsTag
from app.projects.models import IndividualProjectPage
from app.members.models import IndividualMemberPage
from modelcluster.contrib.taggit import ClusterTaggableManager
from home.models import HomePage
from django.core.files.images import ImageFile
from wagtail.images.models import Image
from home.management.migration_helpers import create_image_from_url, create_image_from_local_file, handle_markdown_images, convert_markdown_contents, HOTOSM_LEGACY_SITE_URL, comb_keys


FRONTMATTER_FIELD_TO_NEWS_FIELD_DICT = {
    "date": ("date", lambda date: date),
    "Person": ("authors", lambda authors: handle_authors(authors)),
    "Feature Image": ("image", lambda image: create_image_from_url(HOTOSM_LEGACY_SITE_URL + image, image)),
    "Summary Text": ("intro", lambda intro: f"<p>{intro}</p>"),
    "Project": ("related_projects", lambda projects: handle_projects(projects)),
    "Projects": ("related_projects", lambda projects: handle_projects(projects)),
}


def test_create_page():
    streamfield_body = json.dumps([{"type": "text_block", "value": """<h2>youve been tested by a smooth criminal</h2>"""}])

    # test_image_url = create_image_from_url("https://www.serebii.net/pokemon/art/778.png", "mimikyutestimage.png")
    # test_image_local = create_image_from_local_file("thumbsupmigrationtest.jpg", "thumbsupmigrationtest.jpg")

    migrated_category = NewsCategory.objects.all().filter(category_name="Migrated News")

    test = IndividualNewsPage(
        title="MIGRATION TEST NEWS PAGE", intro="i'm tested", article_body=streamfield_body, date=date.today(),
        categories=migrated_category
        )
    test.tags.add("migrated page")
    
    home = NewsOwnerPage.objects.all()[0].get_translation(1)
    home.add_child(instance=test)
    test.save_revision().publish()


def test_markdown_conversion():
    path = "migration_pages/news/2025-03-05-lebanons-recovery-mapping-a-path-from-rubble-to-resilience.markdown"
    # filename = "2025-02-18-rutas-para-el-desarrollo-mapeando-caminos-para-la-conectividad-y-el-desarrollo-en-guatemala.markdown"
    with open(path, 'r') as file:
        create_news_page_from_markdown(file)


def test_random_garbage():
    result: IndividualNewsPage = IndividualNewsPage.objects.live().search("TESTTTTTT").get_queryset()[0]
    projresult: IndividualProjectPage = IndividualProjectPage.objects.live().search("testttttt").get_queryset()[0]
    print(result.related_projects)
    print(dir(result.related_projects))

    for news in projresult.related_news:
        print(news.value.id)
        print()

    # projresult.related_news = [{'type': 'news_page', 'value': result.id}]

    # with transaction.atomic():
    #     projresult.save()
    # print(NewsCategory.objects.all().filter(category_name="Migrated News"))
    # print(type(result.tags))
    # print(dir(result.tags))


def link_projects_post_creation(project_list, news_id):
    for project in project_list:
        projresult: IndividualProjectPage = IndividualProjectPage.objects.live().filter(id=project['value'])[0]

        related_news = []
        if projresult.related_news and not projresult.related_news[0].value:
            projresult.related_news = []
        for news in projresult.related_news:
            related_news += [{'type': 'news_page', 'value': news.value.id}]
        related_news += [{'type': 'news_page', 'value': news_id}]

        projresult.related_news = related_news

        with transaction.atomic():
            projresult.save()


def handle_projects(projects):
    if not isinstance(projects, list):
        return []
    
    project_list = []

    for project in projects:
        results = IndividualProjectPage.objects.live().search(project).get_queryset()
        if len(results):
            project_list += [{"type": "project_page", "value": results[0].get_translation(1).id}]
    
    return project_list


def handle_single_author(author):
    results = IndividualMemberPage.objects.all().search(author).get_queryset()
    if len(results):
        return [{"type": "author", "value": results[0].get_translation(1).id}]
    else:
        return [{"type": "manual_author", "value": author}]


def handle_authors(authors):
    author_list = []

    if not isinstance(authors, list):
        author_list += handle_single_author(authors)
    else:
        for author in authors:
            author_list += handle_single_author(author)
    
    return author_list


def handle_tags(page: IndividualNewsPage, article):
    if not 'tags' in article.keys():
        return
    for tag in article['tags']:
        page.tags.add(tag)


def markdown_article_to_news_dict(article):
    streamfield_body = json.dumps(convert_markdown_contents(article.content))

    categories = NewsCategory.objects.all().filter(category_name="Migrated News")

    news_dict = {
        "title": article['title'],
        "article_body": streamfield_body,
        "categories": categories,
    }

    for key in FRONTMATTER_FIELD_TO_NEWS_FIELD_DICT.keys():
        if key in article.keys():
            field, func = FRONTMATTER_FIELD_TO_NEWS_FIELD_DICT[key]
            news_dict[field] = func(article[key])

    return news_dict


def create_news_page_from_markdown(file):
    article = frontmatter.load(file)
    if not 'title' in article.keys():
        return
    
    news_dict = markdown_article_to_news_dict(article)
    
    page = IndividualNewsPage(**news_dict)
    handle_tags(page, article)

    owner = NewsOwnerPage.objects.all()[0].get_translation(1)
    owner.add_child(instance=page)
    revision = page.save_revision()
    
    if 'related_projects' in news_dict.keys():
        link_projects_post_creation(news_dict['related_projects'], page.id)

    if 'published' in article.keys() and not article['published']:
        page.unpublish()
        return
    revision.publish()


def convert_all_news_in_dir(directory):
    for filename in os.listdir(directory):
        if not filename.endswith('.markdown') and not filename.endswith('.md'):
            continue
        with open(f"{directory}/{filename}", 'r') as file:
            create_news_page_from_markdown(file)
            print('Converted:', filename)


def remigrate_news_images(file):
    article = frontmatter.load(file)
    if not 'title' in article.keys() or not 'Feature Image' in article.keys() or ('Feature Image' in article.keys() and not article['Feature Image'].startswith("https://cdn.hotosm.org")):
        return
    
    news = IndividualNewsPage.objects.all().filter(title=article['title'])[0].get_translation(1)

    if news.image:
        return

    image = create_image_from_url(article['Feature Image'], article['Feature Image'])

    news.image = image

    with transaction.atomic():
        news.save()
    
    print("Remigrated:", article['title'])


# this function was for remigrating images in pages that failed to get those images,
# because for some reason a bunch of pages weren't able to get the images from the cdn
def remigrate_news_images_in_dir(directory):
    for filename in os.listdir(directory):
        if not filename.endswith('.markdown') and not filename.endswith('.md'):
            continue
        with open(f"{directory}/{filename}", 'r') as file:
            remigrate_news_images(file)


class Command(BaseCommand):
    help = "Migrates news posts"

    def handle(self, *args, **options):
        self.stdout.write("i'm testing! i'm testing!")
        convert_all_news_in_dir('migration_pages/news/')
        # remigrate_news_images_in_dir('migration_pages/_posts')
