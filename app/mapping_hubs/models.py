from django import forms
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from app.projects.models import IndividualProjectPage
from app.ui.models import CarouselBlock


class ContactLinkStructBlock(StructBlock):
    link_text = CharBlock(required=True)
    link_url = URLBlock(required=False, blank=True)


class ContactLinkBlock(StreamBlock):
    blocks = ContactLinkStructBlock()


class DogearBoxStructBlock(StructBlock):
    title = CharBlock(required=True)
    link_text = CharBlock(required=True)
    link_url = URLBlock(required=False, blank=True)


class DogearBoxBlock(StreamBlock):
    blocks = DogearBoxStructBlock()


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
    learn_more_text = models.CharField(default="Learn More about", help_text="The text preceeding the hub's name in the link text; i.e., if this field is 'Learn More about', the link text for 'Asia-Pacific Hub' would become 'Learn More about Asia-Pacific Hub'.")

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('header_description'),
        FieldPanel('hub_text'),
        FieldPanel('learn_more_text'),
    ]


class IndividualMappingHubPage(Page):
    def get_context(self, request):
        context = super().get_context(request)
        projects = context['page'].get_children()
        projects = projects[0].get_children().filter(locale=context['page'].locale) if projects else None
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
    header_hub_text_white = models.CharField(default="Open Mapping")
    header_hub_text_red = models.CharField(default="Hub")
    header_project_link_text = models.CharField(default="Projects")
    header_project_link_url = models.URLField(blank=True)
    header_news_link_text = models.CharField(default="News")
    header_news_link_url = models.URLField(blank=True)
    header_events_link_text = models.CharField(default="Events")
    header_events_link_url = models.URLField(blank=True)
    header_carousel = StreamField(CarouselBlock(max_num=3, min_num=3), blank=True, use_json_field=True, null=True)

    project_section_title = models.CharField()
    project_section_link_text = models.CharField(blank=True)
    project_section_link_url = models.URLField(blank=True)
    
    news_section_title = models.CharField()
    news_section_description = RichTextField(blank=True)
    news_section_link_text = models.CharField(blank=True)
    news_section_link_url = models.URLField(blank=True)

    events_section_title = models.CharField()
    events_section_description = RichTextField(blank=True)
    events_section_link_text = models.CharField(blank=True)
    events_section_link_url = models.URLField(blank=True)

    dogear_boxes = StreamField(DogearBoxBlock(), blank=True, use_json_field=True, help_text="These are, for example, the 'Grants' and 'Map and Chat Hour' boxes in the Asia-Pacific page. Please only add these in pairs of 2!")

    partners_section_title = models.CharField(default="Meet Our Partners")
    partners_section_link_text = models.CharField(default="View All")
    partners_section_link_url = models.URLField(blank=True)
    partners = ParentalManyToManyField('core.Partner', blank=True)

    contact_section_title = models.CharField(default="Contact Us")
    contact_section_description = RichTextField(blank=True)
    contact_section_links = StreamField(ContactLinkBlock(), blank=True, use_json_field=True)

    subscribe_box_text = models.CharField(blank=True)
    subscribe_box_signup_text = models.CharField(default="Sign Up")
    subscribe_box_signup_link = models.URLField(blank=True)

    explore_section_title = models.CharField(default="Explore Other Hubs")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('main_colour'),
            FieldPanel('main_icon'),
            FieldPanel('main_external_hub_image'),
            FieldPanel('intro'),
            FieldPanel('main_body_text'),
        ], heading="Main"),
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_hub_text_white'),
            FieldPanel('header_hub_text_red'),
            FieldPanel('header_project_link_text'),
            FieldPanel('header_project_link_url'),
            FieldPanel('header_news_link_text'),
            FieldPanel('header_news_link_url'),
            FieldPanel('header_events_link_text'),
            FieldPanel('header_events_link_url'),
            FieldPanel('header_carousel'),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('project_section_title'),
            FieldPanel('project_section_link_text'),
            FieldPanel('project_section_link_url'),
        ], heading="Project"),
        MultiFieldPanel([
            FieldPanel('news_section_title'),
            FieldPanel('news_section_description'),
            FieldPanel('news_section_link_text'),
            FieldPanel('news_section_link_url'),
        ], heading="News"),
        MultiFieldPanel([
            FieldPanel('events_section_title'),
            FieldPanel('events_section_description'),
            FieldPanel('events_section_link_text'),
            FieldPanel('events_section_link_url'),
        ], heading="Events"),
        FieldPanel('dogear_boxes'),
        MultiFieldPanel([
            FieldPanel('partners_section_title'),
            FieldPanel('partners_section_link_text'),
            FieldPanel('partners_section_link_url'),
            FieldPanel("partners", widget=forms.CheckboxSelectMultiple),
        ], heading="Partners"),
        MultiFieldPanel([
            FieldPanel('contact_section_title'),
            FieldPanel('contact_section_description'),
            FieldPanel('contact_section_links'),
        ], heading="Contact"),
        MultiFieldPanel([
            FieldPanel('subscribe_box_text'),
            FieldPanel('subscribe_box_signup_text'),
            FieldPanel('subscribe_box_signup_link'),
        ], heading="Subscription Box"),
        FieldPanel('explore_section_title'),
    ]
