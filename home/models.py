from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, PageChooserBlock, ListBlock, BooleanBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page

from app.impact_areas.models import IndividualImpactAreaPage
from app.mapping_hubs.models import IndividualMappingHubPage
from app.core.models import LinkOrPageBlock

import requests
from django.core.cache import cache


class ActionButtonBlock(StructBlock):
    text = CharBlock(required=True, help_text="Text to display on the button")
    link = LinkOrPageBlock(required=False, blank=True, help_text="URL to link to")


class SlideBlock(StructBlock):
    header = CharBlock(required=True, help_text="Slide header")
    body = CharBlock(required=True, help_text="Slide body")
    action_button = ActionButtonBlock(required=False, help_text="Button to display on the slide")


class CarouselBlock(StreamBlock):
    slides = SlideBlock()


class ThirdNavigationStructBlock(StructBlock):
    title = CharBlock()
    link = LinkOrPageBlock(required=False)


class SecondNavigationStructBlock(StructBlock):
    title = CharBlock()
    link = LinkOrPageBlock(required=False)
    children = StreamBlock([('nav_item',ThirdNavigationStructBlock())], use_json_field=True, null=True, blank=True, required=False)


class NavigationStructBlock(StructBlock):
    title = CharBlock()
    link = LinkOrPageBlock(required=False)
    show_in_footer = BooleanBlock(required=False, help_text="If checked, this item (and its children) will show in the footer's navigation; otherwise, it will not show up.")
    children = StreamBlock([('nav_item',SecondNavigationStructBlock())], use_json_field=True, null=True, blank=True, required=False)


class NavigationBlock(StreamBlock):
    blocks = NavigationStructBlock()


def get_apis(stats):
    responses = cache.get('home_page_stats')

    if not responses:
        responses = stats.raw_data

        for stat in responses:
            if stat['value']['api']:
                api = stat['value']['api'][0]['value']
                try:
                    res = requests.get(str(api['endpoint'])).json()
                    for key in api['key_path']:
                        res = res[str(key['value'])]
                    stat['value']['api'] = res
                except:
                    stat['value']['api'] = None
        
        # the "timeout" here controls how long the api calls are cached for (in seconds).
        # additionally, updating the home page will immediately clear the cache; 
        # this is controlled in the wagtail_hooks.py file in this directory.
        cache.set('home_page_stats', responses, timeout=3600)

    return responses


class APIBlock(StreamBlock):
    api = StructBlock([
        ('name', CharBlock(help_text="This name will be used for caching the result of this API, and as such, should be unique.")),
        ('endpoint', CharBlock(help_text="This is the URL that will be called; should return a JSON object.")),
        ('key_path', StreamBlock([
            ('key', CharBlock())
        ], help_text="This should lead to the value that should be displayed for this API; i.e., if the result of calling the endpoint is a JSON object { 'result': {'stat': 10 } }, this field should have 'result' and 'stat' as keys, in that order, so as to navigate to ['result']['stat']."))
    ])

    class Meta:
        max_num = 1


class StatBlock(StreamBlock):
    stat = StructBlock([
        ('fallback_number', CharBlock(help_text="Displays if no API is given, or if the API call fails. This is a string so for numbers you'll want to format it (i.e., 1300 should be typed as 1.3K).")),
        ('statistic', CharBlock(help_text="Displays as the description of the statistic.")),
        ('tooltip', CharBlock(required=False, help_text="If this field is filled, an info 'i' will appear in this stat block, which will show this text when hovered.")),
        ('api', APIBlock(required=False, help_text="Do not touch this field unless you know what you are doing."))
    ])


class HomePage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        impact_areas = IndividualImpactAreaPage.objects.live().filter(locale=context['page'].locale)
        context['impact_areas'] = impact_areas
        mapping_hubs = IndividualMappingHubPage.objects.live().filter(locale=context['page'].locale)
        context['mapping_hubs'] = mapping_hubs

        responses = get_apis(context['page'].specific.home_stats)

        context['api_responses'] = responses

        return context
    
    max_count = 1
    
    templates = "home/home_page.html"

    # Navigation
    top_navigation_socials = StreamField([
        ('social', StructBlock([
            ('service', CharBlock()),
            ('icon', ImageChooserBlock()),
            ('link', LinkOrPageBlock(required=False)),
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="Social media links to be shown in the topmost navigation bar.")
    top_navigation_links = StreamField([
        ('link', StructBlock([
            ('text', CharBlock()),
            ('link', LinkOrPageBlock(required=False))
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="Links to be shown in the topmost navigation bar.")
    top_navigation_donate_text = models.CharField(default="Donate")
    top_navigation_donate_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    navigation = StreamField(NavigationBlock(), use_json_field=True, null=True, blank=True, help_text="The items of the navigation; this is shown on all pages.")
    navigation_buttons = StreamField([('button', ThirdNavigationStructBlock())], use_json_field=True, null=True, blank=True, help_text="The buttons of the navigation; these show up last in the navbar, and, unlike regular navigation items, show up at all times on medium screens.")
    footer_certifications =  StreamField([
        ('certification', StructBlock([
            ('name', CharBlock()),
            ('icon', ImageChooserBlock()),
            ('link', LinkOrPageBlock(required=False)),
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="Certifications to be shown in the footer.")
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
            ('link', LinkOrPageBlock(required=False))
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="The links which show in the bottom right corner of the footer; Privacy Policy, Terms and Conditions, etc.")
    
    # 404 page
    e404_title = models.CharField(default="Page not found")
    e404_description = models.CharField(default="We're sorry, the page you requested could not be found.")
    e404_links = StreamField([
        ('link', StructBlock([
            ('text', CharBlock()),
            ('link', LinkOrPageBlock(required=False))
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="Links to be shown on the 404 page.")

    paginator_previous = models.CharField(default="Previous")
    paginator_next = models.CharField(default="Next")

    social_share_links = StreamField([
        ('social', StructBlock([
            ('icon', ImageChooserBlock()),
            ('link', URLBlock(required=False)),
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="These links will be shown in pages which have a sharing widget; link URLs should be the respective social media site's share link, with the place share message's content being replaced with {}. For example, Twitter's share link would be 'https://twitter.com/intent/tweet?text={}'.")

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
    home_stats = StreamField(StatBlock(), use_json_field=True, blank=True)

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
    view_all_programs_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    highlighted_programs_description = RichTextField(blank=True)
    highlighted_programs = StreamField([('program', PageChooserBlock(page_type="programs.IndividualProgramPage"))], use_json_field=True, null=True, blank=True)
    impact_areas_title = models.CharField(default="Impact Areas")
    impact_areas_description = RichTextField(blank=True)
    impact_areas_learn_more = models.CharField(default="Learn More")

    who_we_are_intro_title = RichTextField(blank=True, help_text="Any text written in bold will be displayed as red in this title.", features=['bold'])
    who_we_are_intro_description = RichTextField(blank=True)
    who_we_are_button_text = models.CharField(default="Who We Are")
    who_we_are_button_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
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
    mapping_hubs_link_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
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
    tools_resources_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

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
    get_involved_button_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    partner_with_us_button_text = models.CharField(default="Partner With Us")
    partner_with_us_button_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    news_title = models.CharField(default="News")
    view_all_news_text = models.CharField(default="View all news")
    view_all_news_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
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
            MultiFieldPanel([
                FieldPanel('top_navigation_socials'),
                FieldPanel('top_navigation_links'),
                FieldPanel('top_navigation_donate_text'),
                FieldPanel('top_navigation_donate_url'),
                FieldPanel('navigation'),
                FieldPanel('navigation_buttons'),
                FieldPanel('footer_certifications'),
                FieldPanel('footer_bottom_copyright'),
                FieldPanel('footer_bottom_links'),
            ], heading="Navigation"),
            MultiFieldPanel([
                FieldPanel('e404_title'),
                FieldPanel('e404_description'),
                FieldPanel('e404_links'),
            ], heading="404 Page"),
            MultiFieldPanel([
                FieldPanel('paginator_previous'),
                FieldPanel('paginator_next'),
            ], heading="Paginator", help_text="This is used in instances where there's a previous/next button; i.e., the news page when flipping through pages."),
            MultiFieldPanel([
                FieldPanel('social_share_links'),
            ], heading="Misc")
        ], heading="Universal items"),
        MultiFieldPanel([
            FieldPanel("image"),
            FieldPanel("hero_text"),
            FieldPanel("hero_cta"),
            FieldPanel("hero_cta_link"),
            FieldPanel("carousel"),
            FieldPanel('home_stats'),
        ], heading="Banner"),
        MultiFieldPanel([
            FieldPanel('our_work_background'),
            FieldPanel('our_work_title'),
            FieldPanel('highlighted_programs_title'),
            FieldPanel('highlighted_programs_description'),
            FieldPanel('highlighted_programs'),
            FieldPanel('view_all_programs_text'),
            FieldPanel('view_all_programs_url'),
            FieldPanel('impact_areas_title'),
            FieldPanel('impact_areas_description'),
        ], heading="Our Work"),
        MultiFieldPanel([
            FieldPanel('who_we_are_intro_title'),
            FieldPanel('who_we_are_intro_description'),
            FieldPanel('who_we_are_button_text'),
            FieldPanel('who_we_are_button_url'),
            FieldPanel('who_we_are_image'),
        ], heading="Who We Are"),
        MultiFieldPanel([
            FieldPanel('mapping_hubs_title'),
            FieldPanel('mapping_hubs_description'),
            FieldPanel('mapping_hubs_link_text'),
            FieldPanel('mapping_hubs_link_link'),
            FieldPanel('mapping_hubs_hub_learn_more'),
            FieldPanel('mapping_hubs_background'),
        ], heading="Mapping Hubs"),
        MultiFieldPanel([
            FieldPanel('tools_resources_image'),
            FieldPanel('tools_resources_title'),
            FieldPanel('tools_resources_description'),
            FieldPanel('tools_resources_button_text'),
            FieldPanel('tools_resources_button_link'),
        ], heading="Tools & Resources"),
        MultiFieldPanel([
            FieldPanel('opportunities_image'),
            FieldPanel('opportunities_title'),
            FieldPanel('opportunities_description'),
            FieldPanel('get_involved_button_text'),
            FieldPanel('get_involved_button_url'),
            FieldPanel('partner_with_us_button_text'),
            FieldPanel('partner_with_us_button_url'),
        ], heading="Opportunities"),
        MultiFieldPanel([
            FieldPanel('news_title'),
            FieldPanel('view_all_news_text'),
            FieldPanel('view_all_news_link'),
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
