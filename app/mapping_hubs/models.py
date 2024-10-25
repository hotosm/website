from django import forms
from django.db import models
from django.db.models import Q

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from app.projects.models import IndividualProjectPage
from app.ui.models import CarouselBlock
from app.core.models import LinkOrPageBlock, Partner


class ContactLinkStructBlock(StructBlock):
    link_text = CharBlock(required=True)
    link_url = LinkOrPageBlock(required=False, blank=True)


class ContactLinkBlock(StreamBlock):
    blocks = ContactLinkStructBlock()


class DogearBoxStructBlock(StructBlock):
    title = CharBlock(required=True)
    description = RichTextBlock(required=False)
    link_text = CharBlock(required=True)
    link_url = LinkOrPageBlock(required=False, blank=True)


class DogearBoxBlock(StreamBlock):
    blocks = DogearBoxStructBlock()


class MappingHubProjectsPage(Page):
    def get_context(self, request):
        context = super().get_context(request)

        parent_hub = context['page'].get_parent()

        base_id = parent_hub.get_translation(1).id

        projects = IndividualProjectPage.objects.live().filter(
            Q(region_hub_list__contains=[{'type': 'region_hub', 'value': base_id}])
        ).filter(locale=context['page'].locale)

        other_hubs_projects = MappingHubProjectsPage.objects.live().filter(locale=context['page'].locale)

        context['projects'] = projects
        context['other_hubs'] = other_hubs_projects
        return context
    
    parent_page_types = [
        'mapping_hubs.IndividualMappingHubPage'
    ]

    load_more_projects_text = models.CharField(default="Load More Projects")

    projects_by_hub_title = models.CharField(default="See Projects by Open Mapping Hub")

    red_box_title = models.CharField(default="See all of HOT's projects")
    red_box_link_text = models.CharField(default="Explore projects")
    red_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="See the many ways to get involved with HOT and open mapping")
    black_box_link_text = models.CharField(default="Get involved")
    black_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('load_more_projects_text'),
        FieldPanel('projects_by_hub_title'),
        FieldPanel('red_box_title'),
        FieldPanel('red_box_link_text'),
        FieldPanel('red_box_link'),
        FieldPanel('black_box_title'),
        FieldPanel('black_box_link_text'),
        FieldPanel('black_box_link'),
    ]


class OpenMappingHubsPage(Page):
    max_count = 1

    subpage_types = [
        'mapping_hubs.IndividualMappingHubPage'
    ]

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image",
    )
    header_description = RichTextField(blank=True)
    hub_text = models.CharField(default="Hub", help_text="The text following a hub's name; i.e., if this field is 'Hub', the title for 'Asia-Pacific' would become 'Asia-Pacific Hub'.")
    learn_more_text = models.CharField(default="Learn More")

    header_hub_text_white = models.CharField(default="Open Mapping")
    header_hub_text_red = models.CharField(default="Hub")
    header_project_link_text = models.CharField(default="Projects")
    header_news_link_text = models.CharField(default="News")
    header_news_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    header_events_link_text = models.CharField(default="Events")
    header_events_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    partners_section_title = models.CharField(default="Meet Our Partners")
    partners_section_link_text = models.CharField(default="View All")
    partners_section_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    contact_section_title = models.CharField(default="Contact Us")

    subscribe_box_signup_text = models.CharField(default="Sign Up")

    explore_section_title = models.CharField(default="Explore Other Hubs")

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('header_description'),
        FieldPanel('hub_text'),
        FieldPanel('learn_more_text'),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('header_hub_text_white'),
                FieldPanel('header_hub_text_red'),
                FieldPanel('header_project_link_text'),
                FieldPanel('header_news_link_text'),
                FieldPanel('header_news_link'),
                FieldPanel('header_events_link_text'),
                FieldPanel('header_events_link'),
            ], heading="Header"),
            FieldPanel('partners_section_title'),
            FieldPanel('partners_section_link_text'),
            FieldPanel('partners_section_link'),
            FieldPanel('contact_section_title'),
            FieldPanel('subscribe_box_signup_text'),
            FieldPanel('explore_section_title'),
        ], heading="Individual Mapping Hub Page"),
    ]


class IndividualMappingHubPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        original_id = context['page'].get_translation(1).id
        context['original_id'] = str(original_id)

        projects = IndividualProjectPage.objects.live().filter(
            Q(region_hub_list__contains=[{'type': 'region_hub', 'value': original_id}])
        ).filter(locale=context['page'].locale)
        context['projects'] = projects
        other_hubs = IndividualMappingHubPage.objects.live().filter(locale=context['page'].locale)
        context['other_hubs'] = other_hubs

        return context

    main_colour = models.CharField(default="#FFFFFF", help_text="The main colour for this mapping hub. This should be a hex code (though any type of CSS colour format will work).")
    main_icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The main icon that should show for this page.",
    )
    main_external_hub_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="A larger image that represents this hub which may be shown on other pages. This should be in a 2:1 aspect ratio; ideally, at least 400x200 pixels.",
    )
    hub_portrait_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The image which shows for this hub on the home page in the 'Open Mapping Hubs' section in large screen sizes. This image should be more of a portrait, centered on what you want to be shown.",
    )
    external_description_long = RichTextField(blank=True, help_text="A long description of the page to be used in external pages, such as the Open Mapping Hubs page.")
    intro = RichTextField(blank=True)
    main_body_text = RichTextField(blank=True)
    
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image",
    )
    header_project_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    header_carousel = StreamField(CarouselBlock(max_num=3, min_num=3), blank=True, use_json_field=True, null=True)

    project_section_title = models.CharField()
    project_section_link_text = models.CharField(blank=True)
    project_section_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    
    news_section_title = models.CharField()
    news_section_description = RichTextField(blank=True)
    news_section_link_text = models.CharField(blank=True)
    news_section_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    events_section_title = models.CharField()
    events_section_description = RichTextField(blank=True)
    events_section_link_text = models.CharField(blank=True)
    events_section_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    dogear_boxes = StreamField(DogearBoxBlock(), blank=True, use_json_field=True, help_text="These are, for example, the 'Grants' and 'Map and Chat Hour' boxes in the Asia-Pacific page. Please only add these in pairs of 2!")

    partner_list = StreamField([('partner', SnippetChooserBlock(Partner))], use_json_field=True, null=True, blank=True)

    contact_section_description = RichTextField(blank=True)
    contact_section_links = StreamField(ContactLinkBlock(), blank=True, use_json_field=True)

    subscribe_box_text = models.CharField(blank=True)
    subscribe_box_signup_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('main_colour'),
            FieldPanel('main_icon'),
            FieldPanel('main_external_hub_image'),
            FieldPanel('hub_portrait_image'),
            FieldPanel('external_description_long'),
            FieldPanel('intro'),
            FieldPanel('main_body_text'),
        ], heading="Main"),
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_project_link'),
            FieldPanel('header_carousel'),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('project_section_title'),
            FieldPanel('project_section_link_text'),
            FieldPanel('project_section_link'),
        ], heading="Project"),
        MultiFieldPanel([
            FieldPanel('news_section_title'),
            FieldPanel('news_section_description'),
            FieldPanel('news_section_link_text'),
            FieldPanel('news_section_link'),
        ], heading="News"),
        MultiFieldPanel([
            FieldPanel('events_section_title'),
            FieldPanel('events_section_description'),
            FieldPanel('events_section_link_text'),
            FieldPanel('events_section_link'),
        ], heading="Events"),
        FieldPanel('dogear_boxes'),
        MultiFieldPanel([
            FieldPanel("partner_list"),
        ], heading="Partners"),
        MultiFieldPanel([
            FieldPanel('contact_section_description'),
            FieldPanel('contact_section_links'),
        ], heading="Contact"),
        MultiFieldPanel([
            FieldPanel('subscribe_box_text'),
            FieldPanel('subscribe_box_signup_url'),
        ], heading="Subscription Box"),
    ]
