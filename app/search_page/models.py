from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField


class SearchPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        keyword = request.GET.get('keyword', '')
        results_list = Page.objects.live().filter(locale=context['page'].locale)
        
        if keyword:
            results_list = results_list.search(keyword).get_queryset()
        
        results_list = results_list.exclude(id__in=[1, 2])

        page = request.GET.get('page', 1)
        paginator = Paginator(results_list, 6)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        
        context['results'] = results
        context['results_paginator'] = paginator
        context['current_page'] = int(page)
        context['keyword'] = keyword
        return context
    
    page_description = "Search results will, by default, attempt to pull from an 'intro' field for the page description; otherwise, it will grab the page's meta search description."

    max_count = 1

    search_text_prefix = models.CharField(default="Your search for")
    search_text_midfix = models.CharField(default="returns")
    search_text_postfix = models.CharField(default="results")

    no_results_text = models.CharField(default="No matching search results for", help_text="This field is a prefix to the current search result in the event no results are found; i.e., if the search keyword was 'Hello' and this field is 'No matching result for', the no-result page would show \"No matching result for \"Hello\"\"")
    no_results_go_back = models.CharField(default="Go Back")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("search_text_prefix"),
            FieldPanel("search_text_midfix"),
            FieldPanel("search_text_postfix"),
        ], heading="Search Result Text", help_text="These combine to make the search result text; i.e., if prefix is 'Your search for', midfix is 'returns', and postfix is 'results', the search result text will be \"Your search for \"example\" returns \"x\" results\""),
        FieldPanel('no_results_text'),
        FieldPanel('no_results_go_back'),
    ]
