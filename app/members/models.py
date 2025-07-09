from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, PageChooserBlock, RichTextBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.projects.models import IndividualProjectPage
from app.news.models import IndividualNewsPage
from app.mapping_hubs.models import IndividualMappingHubPage
from wagtail.search import index
from wagtailmarkdown.fields import MarkdownField
from wagtailmarkdown.blocks import MarkdownBlock

from app.core.models import LinkOrPageBlock

class WebLinkStructBlock(StructBlock):
    link_text = CharBlock(required=True)
    link_url = URLBlock(required=False, blank=True)


class WebLinkBlock(StreamBlock):
    blocks = WebLinkStructBlock()


class MemberGroupOwnerPage(Page):
    max_count = 1

    subpage_types = [
        'members.MemberGroupPage'
    ]

    applied_text = models.CharField(default="applied", help_text="This will be a suffix to a number, used to indicate how many filters are applied currently in some field.")
    search_placeholder = models.CharField(default="Search by name")
    filter_by_country = models.CharField(default="Filter by Country")
    sort_by_titlea = models.CharField(default="Sort by Name Alphabetical")
    sort_by_titlez = models.CharField(default="Sort by Name Reverse Alphabetical")
    search_button_text = models.CharField(default="Search")
    remove_filters_text = models.CharField(default="Remove All Filters")

    load_more_text = models.CharField(default="Load more", help_text="This will be a prefix to the title of the page; i.e., if the page title is 'Voting members', and this field is 'Load more', this will end up appearing as 'Load more Voting members'.")

    view_all_text = models.CharField(default="View all")

    footer_box_title = models.CharField(default="Work for HOT")
    footer_box_description = RichTextField(blank=True)
    footer_box_button_text = models.CharField(default="Check our Job Opportunities")
    footer_box_button_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('applied_text'),
            FieldPanel('search_placeholder'),
            FieldPanel('filter_by_country'),
            FieldPanel('sort_by_titlea'),
            FieldPanel('sort_by_titlez'),
            FieldPanel('search_button_text'),
            FieldPanel('remove_filters_text'),
        ], heading="Search options"),
        FieldPanel('load_more_text'),
        FieldPanel('view_all_text'),
        MultiFieldPanel([
            FieldPanel('footer_box_title'),
            FieldPanel('footer_box_description'),
            FieldPanel('footer_box_button_text'),
            FieldPanel('footer_box_button_url'),
        ], heading="Footer box"),
    ]


class MemberGroupPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        members = IndividualMemberPage.objects.live().filter(
            Q(member_groups__contains=[{'type': 'member_group', 'value': { 'group': context['page'].get_translation(1).id }}])
        ).filter(locale=context['page'].locale)

        keyword = request.GET.get('keyword', '')

        if keyword:
            members = members.filter(title__icontains=keyword)
            # members = members.search(keyword, fields=["title"]).get_queryset()
        
        hubs = IndividualMappingHubPage.objects.live().filter(locale=context['page'].get_translation(1).locale)
        query = Q()
        for hub in hubs:
            if request.GET.get("hub" + str(hub.id), ''):
                query = query | Q(location_hub=hub)
        members = members.filter(query).distinct()

        match request.GET.get('sort', ''):
            case 'sort.titlea':
                members = members.order_by('title')
            case 'sort.titlez':
                members = members.order_by('-title')
            case _:
                members = members.order_by('title')

        page = request.GET.get('page', 1)
        paginator = Paginator(members, 12)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            members = paginator.page(page)
        except PageNotAnInteger:
            members = paginator.page(1)
        except EmptyPage:
            members = paginator.page(paginator.num_pages)

        context['members'] = members
        context['hubs'] = hubs
        context['groups'] = MemberGroupPage.objects.live().filter(locale=context['page'].locale).exclude(id=context['page'].id)

        return context
    
    parent_page_type = [
        'members.MemberGroupOwnerPage'
    ]

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    intro = RichTextField(blank=True, help_text="Appears in the header.")

    body_intro = RichTextField(blank=True)
    body_description = RichTextField(blank=True)

    show_search_options = models.BooleanField(default=True)
    desktop_size_items_per_row = models.SmallIntegerField(default=6, help_text="The number of members shown per row on desktop sizes.", validators=[
        MinValueValidator(4),
        MaxValueValidator(8),
    ])
    position_shown = models.BooleanField(default=False)
    hub_shown = models.BooleanField(default=False)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('body_intro'),
        FieldPanel('body_description'),
        FieldPanel('show_search_options'),
        FieldPanel('desktop_size_items_per_row'),
        FieldPanel('position_shown'),
        FieldPanel('hub_shown'),
    ]


class MemberOwnerPage(Page):
    max_count = 1

    on_the_web_title = models.CharField(default="On the Web")
    posts_title = models.CharField(default="Posts")
    project_contribution_title = models.CharField(default="Project Contribution")
    fallback_avatar = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="If a member doesn't have a profile picture set, this image will show instead.",
    )

    content_panels = Page.content_panels + [
        FieldPanel('on_the_web_title'),
        FieldPanel('posts_title'),
        FieldPanel('project_contribution_title'),
        FieldPanel('fallback_avatar'),
    ]


class MemberGroupBlock(StructBlock):
    group = PageChooserBlock(page_type="members.MemberGroupPage")
    role = CharBlock(required=False)


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
    member_groups = StreamField([('member_group', MemberGroupBlock())], use_json_field=True, null=True, blank=True)
    position = models.CharField(blank=True)
    location_hub = models.ForeignKey(
        'mapping_hubs.IndividualMappingHubPage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    country = models.CharField(blank=True)
    body = StreamField([
        ('text_block', RichTextBlock(features=[
        'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ])),
        ('md_block', MarkdownBlock())
    ], use_json_field=True, null=True, blank=True)
    on_the_web_links = StreamField(WebLinkBlock(), blank=True, use_json_field=True)
    
    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('search_description'),
        index.SearchField('body'),
        index.FilterField('member_groups'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('image'),
        FieldPanel('member_groups'),
        FieldPanel('position'),
        FieldPanel('location_hub'),
        FieldPanel('country'),
        FieldPanel('body'),
        FieldPanel('on_the_web_links'),
    ]
