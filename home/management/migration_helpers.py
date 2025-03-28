from django.core.files.images import ImageFile
from wagtail.images.models import Image
from io import BytesIO
from urllib.request import urlopen
import re
import os
import frontmatter


MARKDOWN_IMAGE_REGEX = "(!\[.*\]\((\/uploads\/(.*))\))"
MARKDOWN_IMAGE_HTML_REGEX = '(!\[(.*)\]\((\/uploads\/([^\)]*))\)|<img.*src="(\/uploads\/(.*?))".*?alt="(.*?)".*?>|<img.*src="(https:\/\/www\.hotosm\.org\/uploads\/(.*?))".*?alt="(.*?)".*?>)'
HOTOSM_LEGACY_SITE_URL = "https://www.hotosm.org"


def create_image_from_bytes(image_bytes: bytes, image_name: str, image_title: str = "") -> Image:
    image_title = image_title if image_title else image_name

    img_file = ImageFile(BytesIO(image_bytes), name=image_name)

    image = Image(
        title=image_name,
        file=img_file,
    )
    image.save()
    image.tags.add("migratedimage")

    return image


"""
please ensure that image_name has a file extension and that it matches
the file extension of the image from the path
"""
def create_image_from_local_file(path: str, image_name: str, image_title: str = "") -> Image:
    with open(path, 'rb') as img:
        img_bytes = img.read()
        image = create_image_from_bytes(img_bytes, image_name, image_title)

        return image


"""
please ensure that image_name has a file extension and that it matches
the file extension of the image's url
"""
def create_image_from_url(url: str, image_name: str, image_title: str = "") -> Image:
    if url.startswith('/uploads'):
        url = HOTOSM_LEGACY_SITE_URL + url
    
    failed = False

    try:
        img_bytes = urlopen(url).read()
    except:
        img_bytes = urlopen("https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png").read()
        failed = True

    image = create_image_from_bytes(img_bytes, image_name, image_title)
    if failed:
        image.tags.add("failedmigrationimage")

    return image


def handle_markdown_images(article: str):
    results = re.findall(MARKDOWN_IMAGE_HTML_REGEX, article)
    image_sets = []

    for result in results:
        fullmatch, md_alt, md_link, md_name, img_ablink, img_abalt, img_abname, img_htlink, img_htalt, img_htname = result

        link = ""
        alt = ""
        filename = ""

        if md_link:
            link = HOTOSM_LEGACY_SITE_URL + md_link
            alt = md_alt
            filename = md_name
        elif img_ablink:
            link = HOTOSM_LEGACY_SITE_URL + img_ablink
            alt = img_abalt
            filename = img_abname
        elif img_htlink:
            link = img_htlink
            alt = img_htalt
            filename = img_htname
        
        alt = alt if alt else filename

        img = create_image_from_url(link, filename, alt)
        
        markdown_embed = f"![{alt}](image:{img.pk})"
        
        image_sets += [(fullmatch, markdown_embed)]

    return image_sets


def convert_markdown_contents(article: str):
    streamfield_body = []

    image_sets = handle_markdown_images(article)

    for fullmatch, embed in image_sets:
        article = article.replace(fullmatch, embed, 1)

    streamfield_body += [{"type": "md_block", "value": article}]

    return streamfield_body


def comb_keys(directory, keys = None):
    if not keys:
        keys = set()
    
    test = {}

    for filename in os.listdir(directory):
        if not filename.endswith('.markdown') and not filename.endswith('.md'):
            continue
        with open(f"{directory}/{filename}", 'r') as file:
            article = frontmatter.load(file)
            if 'Project' in article.keys():
                print("Project", article['Project'])
            if 'Projects' in article.keys():
                print("Projectssss", article['Projects'])
                # for ia in article['Impact Area']:
                #     test.add(ia)
            # tester = "Tools"
            # if tester in article.keys():
            #     print(filename)
            #     print(article[tester])
            #     print()
            #     for tool in article[tester]:
            #         if 'tool' in tool.keys():
            #             try:
            #                 test.add(tool['tool'])
            #             except:
            #                 pass
            for key in article.keys():
                keys.add(key)
                # if not key in test.keys():
                #     test[key] = 0
                # test[key] += 1
    
    # print(test)

    return keys
