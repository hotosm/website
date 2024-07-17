from django.db import models

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from app.core.models import LinkOrPageBlock


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
