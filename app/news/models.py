from django import forms
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.search import index

from app.core.models import LinkOrPageBlock
from app.mapping_hubs.models import IndividualMappingHubPage


class NewsOwnerPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        base_locale = context['page'].get_translation(1).locale

        keyword = request.GET.get('keyword', '')
        news_list = IndividualNewsPage.objects.live().filter(locale=base_locale)
        
        if keyword:
            news_list = news_list.search(keyword).get_queryset()

        categories = NewsCategory.objects.all()
        tags = [x[4:] for x in request.GET.keys() if x.startswith("tag.")]
        query = Q()
        for category in categories:
            if request.GET.get("cat" + str(category.id), ''):
                query = query | Q(categories=category)
        news_list = news_list.filter(query).distinct()
        
        query = Q()
        for tag in tags:
            query = query | Q(tags__name=tag)
        news_list = news_list.filter(query).distinct()

        hubs = IndividualMappingHubPage.objects.live().filter(locale=base_locale)
        query = Q()
        for hub in hubs:
            if request.GET.get(f"hub{hub.id}", ''):
                query = query | Q(associated_hubs__contains=[{'type': 'region_hub', 'value': hub.id }])
        news_list = news_list.filter(query).distinct()

        match request.GET.get('sort', ''):
            case 'sort.new':
                news_list = news_list.order_by('-date')
            case 'sort.old':
                news_list = news_list.order_by('date')
            case 'sort.titlea':
                news_list = news_list.order_by('title')
            case 'sort.titlez':
                news_list = news_list.order_by('-title')
            case _:
                news_list = news_list.order_by('-date')

        page = request.GET.get('page', 1)
        paginator = Paginator(news_list, 6)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        
        context['news'] = news
        context['news_paginator'] = paginator
        context['current_page'] = int(page)
        context['categories'] = categories
        context['hubs'] = hubs
        return context
    
    max_count = 1

    subpage_types = [
        'news.IndividualNewsPage'
    ]

    authors_posted_by_text = models.CharField(default="Posted by", help_text="The text which appears prior to the authors names; with 'posted by', the text displays as 'posted by [author]'.")
    authors_posted_on_text = models.CharField(default="on", help_text="The text which appears prior to the date; with 'on', it would display as 'on [date]'.")
    related_projects_title = models.CharField(default="Related Projects")
    related_news_title = models.CharField(default="Related News")
    view_all_news_text = models.CharField(default="View all News")
    view_all_news_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    news_read_more_text = models.CharField(default="Read More")
    categories_title = models.CharField(default="Categories")
    tags_title = models.CharField(default="Tags")
    hubs_title = models.CharField(default="Associated Hubs")

    applied_text = models.CharField(default="applied", help_text="This will be a suffix to a number, used to indicate how many filters are applied currently in some field.")
    keyword_search_hint = models.CharField(default="Search by keyword")
    filter_by_hub = models.CharField(default="Filter by Hub")
    category_select = models.CharField(default="Select Categories")
    sort_by_new = models.CharField(default="Sort by New")
    sort_by_old = models.CharField(default="Sort by Old")
    sort_by_titlea = models.CharField(default="Sort by Title Alphabetical")
    sort_by_titlez = models.CharField(default="Sort by Title Reverse Alphabetical")
    enter_tag_hint = models.CharField(default="Enter tag")
    search_button_text = models.CharField(default="Search")
    remove_filters_text = models.CharField(default="Remove All Filters")
    results_text = models.CharField(default="Results")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('applied_text'),
            FieldPanel('keyword_search_hint'),
            FieldPanel('filter_by_hub'),
            FieldPanel('category_select'),
            FieldPanel('sort_by_new'),
            FieldPanel('sort_by_old'),
            FieldPanel('sort_by_titlea'),
            FieldPanel('sort_by_titlez'),
            FieldPanel('enter_tag_hint'),
            FieldPanel('search_button_text'),
            FieldPanel('remove_filters_text'),
            FieldPanel('results_text'),
        ], heading="News Search Page"),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel("authors_posted_by_text"),
                FieldPanel("authors_posted_on_text"),
            ], heading="Info"),
            MultiFieldPanel([
                FieldPanel('related_projects_title'),
                FieldPanel('related_news_title'),
                FieldPanel('view_all_news_text'),
                FieldPanel('view_all_news_link'),
                FieldPanel('news_read_more_text'),
                FieldPanel('categories_title'),
                FieldPanel('tags_title'),
            ], heading="Sidebar"),
        ], heading="Individual News Page"),
    ]


@register_snippet
class NewsCategory(models.Model):
    category_name = models.CharField()

    panels = [
        FieldPanel("category_name")
    ]

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name_plural = "News Categories"


class NewsTag(TaggedItemBase):
    content_object = ParentalKey(
        'IndividualNewsPage',
        related_name="tagged_items",
        on_delete=models.CASCADE
    )


class IndividualNewsPage(Page):
    parent_page_type = [
        'news.NewsOwnerPage'
    ]

    authors = StreamField([('author', PageChooserBlock(page_type="members.IndividualMemberPage"))], use_json_field=True, null=True, blank=True)

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Cover image"
    )

    intro = RichTextField(blank=True)

    date = models.DateField(help_text="Post date")

    article_body = StreamField([
        ('text_block', RichTextBlock(features=[
        'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote'
        ]))
    ], use_json_field=True, null=True, blank=True)

    related_projects = StreamField([
        ('project_page', PageChooserBlock(page_type="projects.IndividualProjectPage"))
    ], use_json_field=True, null=True, blank=True)

    related_news = StreamField([
        ('news_page', PageChooserBlock(page_type="news.IndividualNewsPage"))
    ], use_json_field=True, null=True, blank=True)

    categories = ParentalManyToManyField('news.NewsCategory', blank=True)

    tags = ClusterTaggableManager(through=NewsTag, blank=True)

    associated_hubs = StreamField([('region_hub', PageChooserBlock(page_type="mapping_hubs.IndividualMappingHubPage"))], use_json_field=True, null=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('intro'),
        index.SearchField('search_description'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("authors"),
            FieldPanel("date"),
        ], heading="Info"),
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("intro"),
            FieldPanel("article_body"),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('related_projects'),
            FieldPanel('related_news'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
            FieldPanel('associated_hubs'),
        ], heading="Sidebar"),
    ]
