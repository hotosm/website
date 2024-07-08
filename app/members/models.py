from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, PageChooserBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from django.db.models import Q
from app.projects.models import IndividualProjectPage
from app.news.models import IndividualNewsPage
from wagtail.search import index

class WebLinkStructBlock(StructBlock):
    link_text = CharBlock(required=True)
    link_url = URLBlock(required=False, blank=True)


class WebLinkBlock(StreamBlock):
    blocks = WebLinkStructBlock()


class MemberOwnerPage(Page):
    max_count = 1

    on_the_web_title = models.CharField(default="On the Web")
    posts_title = models.CharField(default="Posts")
    project_contribution_title = models.CharField(default="Project Contribution")

    content_panels = Page.content_panels + [
        FieldPanel('on_the_web_title'),
        FieldPanel('posts_title'),
        FieldPanel('project_contribution_title'),
    ]

"""
This page should only be created as a child of a MemberOwnerPage!
Its template depends on fields from the MemberOwnerPage in order
to create one unifying place where unchanging fields may be modified.
"""
class IndividualMemberPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        news_posts = IndividualNewsPage.objects.live().filter(
            Q(authors__contains=[{'type': 'author', 'value': context['page'].id}])
        ).filter(locale=context['page'].locale)
        project_contributions = IndividualProjectPage.objects.live().filter(
            Q(project_contributors__contains=[{'type': 'contributor', 'value': context['page'].id}])
        ).filter(locale=context['page'].locale)

        context['posts'] = news_posts
        context['contributions'] = project_contributions

        return context

    parent_page_type = [
        'members.MemberOwnerPage'
    ]

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="An image of the member",
    )
    position = models.CharField()
    location_hub = models.ForeignKey(
        'mapping_hubs.IndividualMappingHubPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    intro = RichTextField()
    on_the_web_links = StreamField(WebLinkBlock(), blank=True, use_json_field=True)

    
    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('search_description'),
        index.SearchField('intro'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('position'),
        FieldPanel('location_hub'),
        FieldPanel('intro'),
        FieldPanel('on_the_web_links'),
    ]
