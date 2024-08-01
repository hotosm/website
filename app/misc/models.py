from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from app.core.models import LinkOrPageBlock


class CodeOfConductPage(Page):
    max_count = 1

    intro = RichTextField(blank=True)

    short_version_title = models.CharField(default="Short Version")
    short_version_body = RichTextField(blank=True)

    full_version_title = models.CharField(default="Full Version")
    full_version_body = RichTextField(blank=True)

    complaint_handling_title = models.CharField(default="Complaint Handling Process")
    complaint_handling_body = RichTextField(blank=True)

    our_policies_title = models.CharField(default="Our Policies")
    our_policies_links = StreamField([
        ('blocks', StructBlock([
            ('text', CharBlock()),
            ('link', LinkOrPageBlock())
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="Links to be shown under the Our Policies section.")

    question_block_title = models.CharField(default="Have a question about the code of conduct?")
    question_block_button_text = models.CharField(default="Contact Community Working Group")
    question_block_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('short_version_title'),
            FieldPanel('short_version_body'),
            FieldPanel('full_version_title'),
            FieldPanel('full_version_body'),
            FieldPanel('complaint_handling_title'),
            FieldPanel('complaint_handling_body'),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('our_policies_title'),
            FieldPanel('our_policies_links'),
            FieldPanel('question_block_title'),
            FieldPanel('question_block_button_text'),
            FieldPanel('question_block_button_link'),
        ], heading="Sidebar"),
    ]


class PrivacyPolicyPage(Page):
    max_count = 1

    intro = RichTextField(blank=True)
    brief_body_text = RichTextField(blank=True)
    table_of_contents_title = models.CharField(default="This Privacy Policy Contains the Following Sections:")
    body_sections = StreamField([
        ('blocks', StructBlock([
            ('title', CharBlock()),
            ('body', RichTextBlock())
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="Sections to be shown in the body following the table of contents; these sections will automatically populate the table of contents.")

    our_policies_title = models.CharField(default="Our Policies")
    our_policies_links = StreamField([
        ('blocks', StructBlock([
            ('text', CharBlock()),
            ('link', LinkOrPageBlock())
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="Links to be shown under the Our Policies section.")

    question_block_title = models.CharField(default="Have a question about the privacy policy?")
    question_block_button_text = models.CharField(default="Contact HOT")
    question_block_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('brief_body_text'),
            FieldPanel('table_of_contents_title'),
            FieldPanel('body_sections'),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('our_policies_title'),
            FieldPanel('our_policies_links'),
            FieldPanel('question_block_title'),
            FieldPanel('question_block_button_text'),
            FieldPanel('question_block_button_link'),
        ], heading="Sidebar"),
    ]


class JoinOurConversationPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    intro = RichTextField(blank=True, help_text="This is shown in the header.")

    get_connected_title = models.CharField(default="Get Connected!")
    get_connected_blocks = StreamField([
        ('blocks', StructBlock([
            ('icon', ImageChooserBlock()),
            ('title', CharBlock()),
            ('description', RichTextBlock())
        ]))
    ], max_num=3, use_json_field=True, null=True, blank=True, help_text="Blocks to be shown under the Get Connected section.")

    code_of_conduct_title = models.CharField(default="Please read our Code of Conduct")
    code_of_conduct_link_text = models.CharField(default="Code of Conduct")
    code_of_conduct_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    red_box_title = models.CharField(default="Join a working group")
    red_box_link_text = models.CharField(default="Working Groups")
    red_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="Contact a mapping community")
    black_box_link_text = models.CharField(default="Community Contact")
    black_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('get_connected_title'),
        FieldPanel('get_connected_blocks'),
        MultiFieldPanel([
            FieldPanel('code_of_conduct_title'),
            FieldPanel('code_of_conduct_link_text'),
            FieldPanel('code_of_conduct_link_url'),
        ], heading="Code of Conduct"),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Dogear Boxes"),
    ]


class WorkingGroupLinkBlock(StructBlock):
    text = CharBlock()
    link = URLBlock(required=False)


class WorkingGroupBlock(StructBlock):
    title = CharBlock()
    description = RichTextBlock()
    links = StreamBlock([('link', WorkingGroupLinkBlock())])


class WorkingGroupsPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    intro = RichTextField(blank=True, help_text="This is shown in the header.")

    working_groups = StreamField([('working_group', WorkingGroupBlock())], use_json_field=True, null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('intro'),
        FieldPanel('working_groups'),
    ]


class DataPrinciplesPage(Page):
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

    body_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Body image"
    )
    body_text = RichTextField(blank=True)

    info_blocks = StreamField([
        ('blocks', StructBlock([
            ('icon', ImageChooserBlock()),
            ('title', CharBlock()),
            ('description', RichTextBlock())
        ]))
    ], use_json_field=True, null=True, blank=True)

    footer_text = RichTextField(blank=True)
    footer_button_text = models.CharField(default="View the Principles as a Presentation")
    footer_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body_image'),
            FieldPanel('body_text'),
            FieldPanel('info_blocks'),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('footer_text'),
            FieldPanel('footer_button_text'),
            FieldPanel('footer_button_link'),
        ], heading="Footer"),
    ]
