from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from app.core.models import LinkOrPageBlock


class IndividualTechStackPage(Page):
    parent_page_types = [
        'tech.TechProductSuitePage'
    ]

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    intro = RichTextField(blank=True)
    body_text = RichTextField(blank=True)

    info_blocks = StreamField([
        ('blocks', StructBlock([
            ('title', CharBlock()),
            ('description', RichTextBlock())
        ]))
    ], use_json_field=True, null=True, blank=True)

    section_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    section_title = models.CharField(blank=True)
    section_intro = RichTextField(blank=True)
    section_description = RichTextField(blank=True)

    link_blocks = StreamField([
        ('blocks', StructBlock([
            ('title', CharBlock()),
            ('linktext', CharBlock()),
            ('linkurl', LinkOrPageBlock()),
        ]))
    ], use_json_field=True, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('body_text'),
        FieldPanel('info_blocks'),
        MultiFieldPanel([
            FieldPanel('section_image'),
            FieldPanel('section_title'),
            FieldPanel('section_intro'),
            FieldPanel('section_description'),
        ], heading="Body Section"),
        FieldPanel('link_blocks'),
    ]


class TechProductSuitePage(Page):
    subpage_types = [
        'tech.IndividualTechStackPage'
    ]

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

    tech_principles_title = models.CharField(default="Tech Principles")
    tech_principle_blocks = StreamField([
        ('blocks', StructBlock([
            ('title', CharBlock()),
            ('description', RichTextBlock())
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="Blocks to be shown under the Tech Principles section.")

    product_suite_title = models.CharField(default="Product Suite")
    product_suite_learn_more_text = models.CharField(default="Learn more about", help_text="Prefix text to be shown in page previews for the product suite section; if the page being previewed is named 'Tasking Manager', and this field is 'Learn more about', they would combine to be 'Learn more about Tasking Manager'.")

    red_box_title = models.CharField(default="HOT GitHub")
    red_box_link_text = models.CharField(default="View HOT's GitHub")
    red_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="Tech News")
    black_box_link_text = models.CharField(default="View tech news")
    black_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    go_back_text = models.CharField(default="Go Back to Tools & Resources")
    go_back_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    tech_stack_links_title = models.CharField(default="Links")
    tech_stack_cta_title = models.CharField(blank=True)
    tech_stack_cta_description = RichTextField(blank=True)
    tech_stack_cta_button_link_text = models.CharField(blank=True)
    tech_stack_cta_button_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    tech_stack_go_back_text = models.CharField(default="Go Back to", help_text="Prefix text to be shown at the bottom of page for going back; this will always refer to the parent page, so if the parent page is 'Tools & Resources', and this field is 'Go Back to', they would combine to be 'Go Back to Tools & Resources'.")

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('tech_principles_title'),
        FieldPanel('tech_principle_blocks'),
        FieldPanel('product_suite_title'),
        FieldPanel('product_suite_learn_more_text'),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Dogear Boxes"),
        MultiFieldPanel([
            FieldPanel('go_back_text'),
            FieldPanel('go_back_link'),
        ], heading="Go Back"),
        MultiFieldPanel([
            FieldPanel('tech_stack_links_title'),
            MultiFieldPanel([
                FieldPanel('tech_stack_cta_title'),
                FieldPanel('tech_stack_cta_description'),
                FieldPanel('tech_stack_cta_button_link_text'),
                FieldPanel('tech_stack_cta_button_link_url'),    
            ], heading="Call to Action"),
            FieldPanel('tech_stack_go_back_text'),
        ], heading="Individual Tech Stack Page"),
    ]
