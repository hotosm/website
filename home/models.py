from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, PageChooserBlock, ListBlock, BooleanBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from app.impact_areas.models import IndividualImpactAreaPage
from app.mapping_hubs.models import IndividualMappingHubPage


class ActionButtonBlock(StructBlock):
    text = CharBlock(required=True, help_text="Text to display on the button")
    link = URLBlock(required=False, blank=True, help_text="URL to link to")


class SlideBlock(StructBlock):
    header = CharBlock(required=True, help_text="Slide header")
    body = CharBlock(required=True, help_text="Slide body")
    action_button = ActionButtonBlock(required=False, help_text="Button to display on the slide")


class CarouselBlock(StreamBlock):
    slides = SlideBlock()


class ThirdNavigationStructBlock(StructBlock):
    title = CharBlock()
    link_url = URLBlock(required=False, help_text="A link URL or page must be provided; if both are present, the link will default to the page.")
    link_page = PageChooserBlock(required=False, help_text="A link URL or page must be provided; if both are present, the link will default to the page.")


class SecondNavigationStructBlock(StructBlock):
    title = CharBlock()
    link_url = URLBlock(required=False, help_text="A link URL or page must be provided; if both are present, the link will default to the page.")
    link_page = PageChooserBlock(required=False, help_text="A link URL or page must be provided; if both are present, the link will default to the page.")
    children = StreamBlock([('nav_item',ThirdNavigationStructBlock())], use_json_field=True, null=True, blank=True, required=False)


class NavigationStructBlock(StructBlock):
    title = CharBlock()
    link_url = URLBlock(required=False, help_text="A link URL or page must be provided; if both are present, the link will default to the page.")
    link_page = PageChooserBlock(required=False, help_text="A link URL or page must be provided; if both are present, the link will default to the page.")
    show_in_footer = BooleanBlock(required=False, help_text="If checked, this item (and its children) will show in the footer's navigation; otherwise, it will not show up.")
    children = StreamBlock([('nav_item',SecondNavigationStructBlock())], use_json_field=True, null=True, blank=True, required=False)


class NavigationBlock(StreamBlock):
    blocks = NavigationStructBlock()


class HomePage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        impact_areas = IndividualImpactAreaPage.objects.live().filter(locale=context['page'].locale)
        context['impact_areas'] = impact_areas
        mapping_hubs = IndividualMappingHubPage.objects.live().filter(locale=context['page'].locale)
        context['mapping_hubs'] = mapping_hubs
        return context
    
    templates = "home/home_page.html"

    # Navigation
    navigation = StreamField(NavigationBlock(), use_json_field=True, null=True, blank=True, help_text="The items of the navigation; this is shown on all pages.")
    navigation_buttons = StreamField([('button', ThirdNavigationStructBlock())], use_json_field=True, null=True, blank=True, help_text="The buttons of the navigation; these show up last in the navbar, and, unlike regular navigation items, show up at all times on medium screens.")
    footer_candid_seal = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The Candid transparency seal image to be shown in the footer; this is shown on all pages.",
    )
    footer_bottom_copyright = RichTextField(features=['link'], blank=True)
    footer_bottom_links = StreamField([
        ('link', StructBlock([
            ('text', CharBlock()),
            ('url', URLBlock(required=False))
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="The links which show in the bottom right corner of the footer; Privacy Policy, Terms and Conditions, etc.")

    # Hero section
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Banner image",
    )
    hero_text = models.CharField(
        max_length=500,
        blank=False,
        null=True,
        help_text="Write an introduction for the hero/landing page section",
    )
    hero_cta = models.CharField(
        max_length=50, blank=False, null=True, help_text="Write text for the Call to Action button"
    )
    hero_cta_link = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Select a page to link to for the Call to Action button",
    )
    carousel = StreamField(
        CarouselBlock(max_num=3, min_num=3),
        verbose_name="Carousel",
        blank=True,
        use_json_field=True,
    )

    our_work_background = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Background for the entire Our Work section",
    )
    our_work_title = models.CharField(default="Our Work")
    highlighted_programs_title = models.CharField(default="Highlighted Programs")
    view_all_programs_text = models.CharField(default="View all programs")
    view_all_programs_link = models.URLField(blank=True)
    highlighted_programs_description = RichTextField(blank=True)
    highlighted_programs = StreamField([('program', PageChooserBlock(page_type="programs.IndividualProgramPage"))], use_json_field=True, null=True, blank=True)
    impact_areas_title = models.CharField(default="Impact Areas")
    impact_areas_description = RichTextField(blank=True)
    impact_areas_learn_more = models.CharField(default="Learn More")

    who_we_are_intro_title = RichTextField(blank=True, help_text="Any text written in bold will be displayed as red in this title.", features=['bold'])
    who_we_are_intro_description = RichTextField(blank=True)
    who_we_are_button_text = models.CharField(default="Who We Are")
    who_we_are_button_link = models.URLField(blank=True)
    who_we_are_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Who we are image",
    )

    mapping_hubs_title = RichTextField(blank=True, help_text="Any text written in bold will be displayed as red in this title.", features=['bold'])
    mapping_hubs_description = RichTextField(blank=True)
    mapping_hubs_link_text = models.CharField(default="Check out HOT's Open Mapping Hubs")
    mapping_hubs_link_url = models.URLField(blank=True)
    mapping_hubs_hub_learn_more = models.CharField(default="Learn More")
    mapping_hubs_background = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The background that shows in the default info panel for Open Mapping Hubs",
    )

    tools_resources_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Tools and Resources section image",
    )
    tools_resources_title = RichTextField(blank=True, help_text="Any text written in bold will be displayed as red in this title.", features=['bold'])
    tools_resources_description = RichTextField(blank=True)
    tools_resources_button_text = models.CharField(default="Tools & Resources")
    tools_resources_button_url = models.URLField(blank=True)

    opportunities_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Opportunities section image",
    )
    opportunities_title = RichTextField(blank=True, help_text="Any text written in bold will be displayed as red in this title.", features=['bold'])
    opportunities_description = RichTextField(blank=True)
    get_involved_button_text = models.CharField(default="Get Involved")
    get_involved_button_link = models.URLField(blank=True)
    partner_with_us_button_text = models.CharField(default="Partner With Us")
    partner_with_us_button_link = models.URLField(blank=True)

    news_title = models.CharField(default="News")
    view_all_news_text = models.CharField(default="View all news")
    view_all_news_url = models.URLField(blank=True)
    displayed_news = StreamField([
        ('news_page', PageChooserBlock(page_type="news.IndividualNewsPage"))
    ], use_json_field=True, null=True, blank=True, min_num=3, max_num=3)

    subscribe_title = models.CharField(default="Subscribe for Updates & Announcements")
    subscribe_first_name_text = models.CharField(default="First Name")
    subscribe_first_name_field_hint = models.CharField(default="Enter your first name...")
    subscribe_last_name_text = models.CharField(default="Last Name")
    subscribe_last_name_field_hint = models.CharField(default="Enter your last name...")
    subscribe_email_text = models.CharField(default="Email Address")
    subscribe_email_field_hint = models.CharField(default="Enter your email address...")
    subscribe_submit_button_text = models.CharField(default="Submit")
    subscribe_checkbox_text = RichTextField(blank=True, help_text="Ensure that you include a link to the privacy policy within this field.", features=['link'])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('navigation'),
            FieldPanel('navigation_buttons'),
            FieldPanel('footer_candid_seal'),
            FieldPanel('footer_bottom_copyright'),
            FieldPanel('footer_bottom_links'),
        ], heading="Navigation"),
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("hero_text"),
            FieldPanel("hero_cta"),
            FieldPanel("hero_cta_link"),
            FieldPanel("carousel"),
        ], heading="Banner"),
        MultiFieldPanel([
            FieldPanel('our_work_background'),
            FieldPanel('our_work_title'),
            FieldPanel('highlighted_programs_title'),
            FieldPanel('highlighted_programs_description'),
            FieldPanel('highlighted_programs'),
            FieldPanel('view_all_programs_text'),
            FieldPanel('view_all_programs_link'),
            FieldPanel('impact_areas_title'),
            FieldPanel('impact_areas_description'),
        ], heading="Our Work"),
        MultiFieldPanel([
            FieldPanel('who_we_are_intro_title'),
            FieldPanel('who_we_are_intro_description'),
            FieldPanel('who_we_are_button_text'),
            FieldPanel('who_we_are_button_link'),
            FieldPanel('who_we_are_image'),
        ], heading="Who We Are"),
        MultiFieldPanel([
            FieldPanel('mapping_hubs_title'),
            FieldPanel('mapping_hubs_description'),
            FieldPanel('mapping_hubs_link_text'),
            FieldPanel('mapping_hubs_link_url'),
            FieldPanel('mapping_hubs_hub_learn_more'),
            FieldPanel('mapping_hubs_background'),
        ], heading="Mapping Hubs"),
        MultiFieldPanel([
            FieldPanel('tools_resources_image'),
            FieldPanel('tools_resources_title'),
            FieldPanel('tools_resources_description'),
            FieldPanel('tools_resources_button_text'),
            FieldPanel('tools_resources_button_url'),
        ], heading="Tools & Resources"),
        MultiFieldPanel([
            FieldPanel('opportunities_image'),
            FieldPanel('opportunities_title'),
            FieldPanel('opportunities_description'),
            FieldPanel('get_involved_button_text'),
            FieldPanel('get_involved_button_link'),
            FieldPanel('partner_with_us_button_text'),
            FieldPanel('partner_with_us_button_link'),
        ], heading="Opportunities"),
        MultiFieldPanel([
            FieldPanel('news_title'),
            FieldPanel('view_all_news_text'),
            FieldPanel('view_all_news_url'),
            FieldPanel('displayed_news'),
        ], heading="News"),
        MultiFieldPanel([
            FieldPanel('subscribe_title'),
            FieldPanel('subscribe_first_name_text'),
            FieldPanel('subscribe_first_name_field_hint'),
            FieldPanel('subscribe_last_name_text'),
            FieldPanel('subscribe_last_name_field_hint'),
            FieldPanel('subscribe_email_text'),
            FieldPanel('subscribe_email_field_hint'),
            FieldPanel('subscribe_submit_button_text'),
            FieldPanel('subscribe_checkbox_text'),
        ], heading="Email Subscription")
    ]


class BlankInaccessiblePage(Page):
    pass
