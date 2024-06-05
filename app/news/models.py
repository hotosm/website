from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.snippets.models import register_snippet


class NewsOwnerPage(Page):
    max_count = 1

    authors_posted_by_text = models.CharField(default="Posted by", help_text="The text which appears prior to the authors names; with 'posted by', the text displays as 'posted by [author]'.")
    authors_posted_on_text = models.CharField(default="on", help_text="The text which appears prior to the date; with 'on', it would display as 'on [date]'.")
    related_projects_title = models.CharField(default="Related Projects")
    related_news_title = models.CharField(default="Related News")
    view_all_news_text = models.CharField(default="View all News")
    view_all_news_url = models.URLField(blank=True)
    news_read_more_text = models.CharField(default="Read More")
    categories_title = models.CharField(default="Categories")
    tags_title = models.CharField(default="Tags")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("authors_posted_by_text"),
            FieldPanel("authors_posted_on_text"),
        ], heading="Info"),
        MultiFieldPanel([
            FieldPanel('related_projects_title'),
            FieldPanel('related_news_title'),
            FieldPanel('view_all_news_text'),
            FieldPanel('view_all_news_url'),
            FieldPanel('news_read_more_text'),
            FieldPanel('categories_title'),
            FieldPanel('tags_title'),
        ], heading="Sidebar"),
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
        'h1', 'h2', 'h3', 'h4', 'bold', 'italic', 'link', 'ol', 'ul', 'hr', 'document-link', 'image', 'embed', 'code', 'blockquote'
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
        ], heading="Sidebar"),
    ]



