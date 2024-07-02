from django import forms
from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.images.blocks import ImageChooserBlock


class IntroInfoBlock(StructBlock):
    image = ImageChooserBlock()
    title = CharBlock(blank=True)
    description = RichTextBlock(blank=True, required=False)


class TextAndLinkBlock(StructBlock):
    text = CharBlock()
    link = URLBlock(blank=True, required=False)


class OtherPagePreviewBlock(StructBlock):
    image = ImageChooserBlock()
    page = PageChooserBlock()


class WhoWeArePage(Page):
    max_count = 1
    
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    intro = RichTextField(blank=True)
    learn_more_button_text = models.CharField(default="Learn More About Our Living Strategy")
    learn_more_button_url = models.URLField(blank=True)
    intro_info_blocks = StreamField([('info_block', IntroInfoBlock())], use_json_field=True, null=True, blank=True)

    our_approach_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Our approach image"
    )
    our_approach_title = models.CharField(default="Our Approach")
    our_approach_description = models.CharField(blank=True)
    our_approach_button_url = models.URLField(blank=True)
    our_approach_button_text = models.CharField(default="Our Approach")

    our_people_title = models.CharField(default="Our People")
    our_people_description = RichTextField(blank=True)
    our_people_links = StreamField([('link_block', TextAndLinkBlock())], use_json_field=True, null=True, blank=True)

    other_page_preview_blocks = StreamField([('other_page_preview', OtherPagePreviewBlock())], use_json_field=True, null=True, blank=True)

    partners_title = models.CharField(default="Meet Our Partners")
    partners_view_all_text = models.CharField(default="View All Partners")
    partners_view_all_url = models.URLField(blank=True)
    partners = ParentalManyToManyField('core.Partner', blank=True)

    work_hot_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Work for HOT section image",
    )
    work_hot_title = models.CharField(default="Work for HOT")
    work_hot_description = RichTextField(blank=True)
    work_hot_button_text = models.CharField(default="View all Job Opportunities")
    work_hot_button_link = models.URLField(blank=True)

    our_policies_title = models.CharField(default="Our Policies")
    our_policies_description = RichTextField(blank=True)
    our_policies_links = StreamField([('link_block', TextAndLinkBlock())], use_json_field=True, null=True, blank=True)

    red_box_title = models.CharField(default="Annual Reports")
    red_box_description = RichTextField(default="Access our annual report archive.")
    red_box_link_text = models.CharField(default="Check all Annual Reports")
    red_box_link_url = models.URLField(null=True, blank=True)
    black_box_title = models.CharField(default="Our Financial Reports")
    black_box_description = RichTextField(default="Access older financial reports and organization bylaws in our archive.")
    black_box_link_text = models.CharField(default="Check all Financial Reports")
    black_box_link_url = models.URLField(null=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('intro'),
            FieldPanel('learn_more_button_text'),
            FieldPanel('learn_more_button_url'),
            FieldPanel('intro_info_blocks'),
        ], heading="Introduction"),
        MultiFieldPanel([
            FieldPanel('our_approach_image'),
            FieldPanel('our_approach_title'),
            FieldPanel('our_approach_description'),
            FieldPanel('our_approach_button_url'),
            FieldPanel('our_approach_button_text'),
        ], heading="Our Approach"),
        MultiFieldPanel([
            FieldPanel('our_people_title'),
            FieldPanel('our_people_description'),
            FieldPanel('our_people_links'),
        ], heading="Our People"),
        FieldPanel('other_page_preview_blocks'),
        MultiFieldPanel([
            FieldPanel('partners_title'),
            FieldPanel('partners_view_all_text'),
            FieldPanel('partners_view_all_url'),
            FieldPanel('partners', widget=forms.CheckboxSelectMultiple),
        ], heading="Partners"),
        MultiFieldPanel([
            FieldPanel('work_hot_image'),
            FieldPanel('work_hot_title'),
            FieldPanel('work_hot_description'),
            FieldPanel('work_hot_button_text'),
            FieldPanel('work_hot_button_link'),
        ], heading="Work for HOT"),
        MultiFieldPanel([
            FieldPanel('our_policies_title'),
            FieldPanel('our_policies_description'),
            FieldPanel('our_policies_links'),
        ], heading="Our Policies"),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_description'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_description'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Dogear Boxes"),
    ]
