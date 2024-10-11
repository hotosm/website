from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock, EmailBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.contrib.table_block.blocks import TableBlock

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


class DocumentCollectionPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        documents = context['page'].documents
        page = request.GET.get('page', 1)
        paginator = Paginator(documents, 6)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            documents = paginator.page(page)
        except PageNotAnInteger:
            documents = paginator.page(1)
        except EmptyPage:
            documents = paginator.page(paginator.num_pages)
        
        context['documents'] = documents
        context['paginator'] = paginator
        context['current_page'] = int(page)
        return context

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    header_description = RichTextField(blank=True)

    document_access_prefix_text = models.CharField(default="Access", help_text="Text to prefix the name of the document in the link to the document; if the document's title is 'Cool Doc', and this field is 'Access', the link for the document would show as 'Access Cool Doc'.")
    documents = StreamField([
        ('block', StructBlock([
            ('icon', ImageChooserBlock(blank=True, null=True, required=False)),
            ('title', CharBlock()),
            ('link', LinkOrPageBlock()),
            ('description', RichTextBlock(blank=True, null=True, required=False))
        ]))
    ], use_json_field=True, null=True, blank=True)

    sidebar_box_title = models.CharField(blank=True)
    sidebar_box_button_text = models.CharField(blank=True)
    sidebar_box_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_description'),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('document_access_prefix_text'),
            FieldPanel('documents'),
        ], heading="Documents"),
        MultiFieldPanel([
            FieldPanel('sidebar_box_title'),
            FieldPanel('sidebar_box_button_text'),
            FieldPanel('sidebar_box_button_link'),
        ], heading="Sidebar"),
    ]


class ContactUsPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    body_background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Shows behind the entire body"
    )

    global_office_title = models.CharField(default="Global Office")
    global_office_text = RichTextField(blank=True)

    send_message_title = models.CharField(default="Send us a message!")

    first_name_text = models.CharField(default="First Name")
    last_name_text = models.CharField(default="Last Name")
    email_text = models.CharField(default="Email Address")
    subject_text = models.CharField(default="Subject")
    message_text = models.CharField(default="Message")

    first_name_field_text = models.CharField(default="Enter your first name...")
    last_name_field_text = models.CharField(default="Enter your last name...")
    email_field_text = models.CharField(default="Enter your email address...")
    subject_field_placeholder = models.CharField(default="Select")
    subject_field_options = StreamField([
        ('block', StructBlock([
            ('subject', CharBlock(blank=True, null=True, required=False)),
        ]))
    ], use_json_field=True, null=True, blank=True)
    message_field_text = models.CharField(default="Enter your message...")

    submit_button_text = models.CharField(default="Submit")

    inquiries_title = models.CharField(default="Inquiries")
    inquiries_blocks = StreamField([
        ('block', StructBlock([
            ('title', CharBlock(blank=True, null=True, required=False)),
            ('email', EmailBlock(blank=True, null=True, required=False)),
        ]))
    ], use_json_field=True, null=True, blank=True)

    office_locations_title = models.CharField(default="Office Locations")
    office_locations_visit_page_text = models.CharField(default="Visit Page")
    office_locations = StreamField([
        ('block', StructBlock([
            ('title', CharBlock(blank=True, null=True, required=False)),
            ('link', LinkOrPageBlock(blank=True, null=True, required=False)),
            ('description', RichTextBlock(blank=True, null=True, required=False)),
        ]))
    ], use_json_field=True, null=True, blank=True)

    dogear_box_title = models.CharField(default="We want to know what you think about HOT and our work.")
    dogear_box_link_text = models.CharField(default="Send us your feedback")
    dogear_box_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('header_image'),
        FieldPanel('body_background_image'),
        MultiFieldPanel([
            FieldPanel('global_office_title'),
            FieldPanel('global_office_text'),
        ], heading="Global Office"),
        MultiFieldPanel([
            FieldPanel('send_message_title'),
            FieldPanel('submit_button_text'),
            MultiFieldPanel([
                FieldPanel('first_name_text'),
                FieldPanel('last_name_text'),
                FieldPanel('email_text'),
                FieldPanel('subject_text'),
                FieldPanel('message_text'),
            ], heading="Form Headers"),
            MultiFieldPanel([
                FieldPanel('first_name_field_text'),
                FieldPanel('last_name_field_text'),
                FieldPanel('email_field_text'),
                FieldPanel('subject_field_placeholder'),
                FieldPanel('subject_field_options'),
                FieldPanel('message_field_text'),
            ], heading="Form Placeholders"),
        ], heading="Form"),
        MultiFieldPanel([
            FieldPanel('inquiries_title'),
            FieldPanel('inquiries_blocks'),
        ], heading="Inquiries"),
        MultiFieldPanel([
            FieldPanel('office_locations_title'),
            FieldPanel('office_locations_visit_page_text'),
            FieldPanel('office_locations'),
        ], heading="Office Locations"),
        MultiFieldPanel([
            FieldPanel('dogear_box_title'),
            FieldPanel('dogear_box_link_text'),
            FieldPanel('dogear_box_link'),
        ], heading="Dogear Box"),
    ]


class WorkForHotPage(Page):
    max_count = 1

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    header_text = RichTextField(blank=True)

    our_values_title = models.CharField(default="Our Values")
    our_values_text = RichTextField(blank=True)
    our_values_youtube_url = models.URLField(blank=True, help_text="The YouTube link provided should be in the following format: 'https://www.youtube.com/embed/[slug]'. You can get this by right-clicking on the YouTube video player and pressing 'Copy embed code'; this will give you a full embed code, which you will need to take the embed URL from.")
    our_values_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="If a YouTube URL is provided, the video will be prioritised over this image; if there is no URL provided, this image will show."
    )
    our_values_subtitle = models.CharField(blank=True)

    work_culture_title = models.CharField(default="Work Culture & Benefits")
    work_culture_description = RichTextField(blank=True)
    work_culture_youtube_url = models.URLField(blank=True, help_text="The YouTube link provided should be in the following format: 'https://www.youtube.com/embed/[slug]'. You can get this by right-clicking on the YouTube video player and pressing 'Copy embed code'; this will give you a full embed code, which you will need to take the embed URL from.")
    work_culture_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="If a YouTube URL is provided, the video will be prioritised over this image; if there is no URL provided, this image will show."
    )
    work_culture_subtitle = models.CharField(blank=True)

    testimonials_title = models.CharField(default="What Our Staff Say")
    testimonials = StreamField([
        ('block', StructBlock([
            ('description', RichTextBlock(blank=True, null=True, required=False)),
            ('member', PageChooserBlock(page_type="members.IndividualMemberPage", required=False)),
            ('image_override', ImageChooserBlock(required=False)),
            ('name_override', CharBlock(required=False)),
            ('title_override', CharBlock(required=False)),
            ('hub_override', PageChooserBlock(page_type="mapping_hubs.IndividualMappingHubPage", required=False))
        ]))
    ], use_json_field=True, null=True, blank=True, help_text="For any given testimonial, you can choose a member to be displayed, or you can alternatively manually provide the member's details; if both are provided, the manually-entered details will override any details fetched from the member's page.")

    opportunities_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Opportunities image"
    )
    opportunities_title = models.CharField(default="See Our Job Opportunities")
    opportunities_description = RichTextField(blank=True)
    opportunities_button_text = models.CharField(default="See all job opportunities")
    opportunities_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_text'),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('our_values_title'),
            FieldPanel('our_values_text'),
            FieldPanel('our_values_youtube_url'),
            FieldPanel('our_values_image'),
            FieldPanel('our_values_subtitle'),
        ], heading="Our Values"),
        MultiFieldPanel([
            FieldPanel('work_culture_title'),
            FieldPanel('work_culture_description'),
            FieldPanel('work_culture_youtube_url'),
            FieldPanel('work_culture_image'),
            FieldPanel('work_culture_subtitle'),
        ], heading="Work Culture"),
        MultiFieldPanel([
            FieldPanel('testimonials_title'),
            FieldPanel('testimonials'),
        ], heading="Testimonials"),
        MultiFieldPanel([
            FieldPanel('opportunities_image'),
            FieldPanel('opportunities_title'),
            FieldPanel('opportunities_description'),
            FieldPanel('opportunities_button_text'),
            FieldPanel('opportunities_button_link'),
        ], heading="Opportunities"),
    ]


class LivingStrategyPage(Page):
    max_count = 1

    desktop_size_non_full_body_width = models.BooleanField()

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )

    download_title = models.CharField(default="Download our Living Strategy Summary")
    downloads = StreamField([('block', StructBlock([
        ('text', CharBlock()),
        ('link', LinkOrPageBlock(required=False)),
    ]))], use_json_field=True, blank=True)

    description = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('desktop_size_non_full_body_width'),
        FieldPanel('banner_image'),
        FieldPanel('download_title'),
        FieldPanel('downloads'),
        FieldPanel('description'),
    ]


class SalaryFrameworkPage(Page):
    max_count = 1

    intro = RichTextField(blank=True)
    body = StreamField([
        ('text', RichTextBlock()),
        ('table', TableBlock()),
    ], use_json_field=True, blank=True)
    go_back_prefix_text = models.CharField(default="Go Back to", help_text="This text will be a prefix to the parent page of this current page, and the attached link will always go to the parent page; i.e., if this page is a child of the 'Work for HOT' page, and this field is 'Go Back to', the link will read 'Go Back to Work for HOT'.")

    sidebar_block_title = models.CharField(default="HOT's Journey through Salary Transparency")
    sidebar_block_description = RichTextField(blank=True)
    sidebar_block_button_text = models.CharField(default="Read More")
    sidebar_block_button_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('intro'),
            FieldPanel('body'),
            FieldPanel('go_back_prefix_text'),
        ]),
        MultiFieldPanel([
            FieldPanel('sidebar_block_title'),
            FieldPanel('sidebar_block_description'),
            FieldPanel('sidebar_block_button_text'),
            FieldPanel('sidebar_block_button_link'),
        ]),
    ]


class DonatePage(Page):
    max_count = 1

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    banner_description = RichTextField(blank=True)

    intro = RichTextField(blank=True)

    other_ways_to_donate_title = models.CharField(default="Other Ways to Donate")
    other_ways_to_donate = StreamField([
        ('block', StructBlock([
            ('icon', ImageChooserBlock()),
            ('title', CharBlock()),
            ('text', RichTextBlock()),
        ]))
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('banner_image'),
        FieldPanel('banner_description'),
        FieldPanel('intro'),
        FieldPanel('other_ways_to_donate_title'),
        FieldPanel('other_ways_to_donate'),
    ]


class MultimediaPage(Page):
    max_count = 1

    banner_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    intro = RichTextField(blank=True)

    map_title = models.CharField(default="Map Gallery")
    map_view_all_text = models.CharField(default="View all maps")
    map_view_all_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    video_title = models.CharField(default="Videos")
    video_view_all_text = models.CharField(default="View more videos on YouTube")
    video_view_all_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    video_overlay_icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="This icon will show on top of the video previews in this section; this should either be a play button, or nothing at all."
    )
    video_previews = StreamField([
        ('preview', StructBlock([
            ('link', URLBlock(help_text="This link should be in the format of 'https://www.youtube.com/watch?v=[code]', as opposed to a share link.")),
            ('short_desc', CharBlock(required=False, help_text="This will show beneath the image.")),
        ], min_num=8, max_num=8))
    ], use_json_field=True, blank=True)

    image_title = models.CharField(default="Images")
    image_view_all_text = models.CharField(default="View more images on Flickr")
    image_view_all_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    image_previews = StreamField([
        ('preview', StructBlock([
            ('link', URLBlock(required=False, help_text="The link to the image source (if known).")),
            ('image', ImageChooserBlock()),
            ('short_desc', CharBlock(required=False, help_text="This will show beneath the image.")),
        ], min_num=8, max_num=8))
    ], use_json_field=True, blank=True)

    license_title = models.CharField(default="License and Attributions")
    license_block = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('banner_image'),
            FieldPanel('intro'),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('map_title'),
            FieldPanel('map_view_all_text'),
            FieldPanel('map_view_all_link'),
        ], heading="Map"),
        MultiFieldPanel([
            FieldPanel('video_title'),
            FieldPanel('video_view_all_text'),
            FieldPanel('video_view_all_link'),
            FieldPanel('video_overlay_icon'),
            FieldPanel('video_previews'),
        ], heading="Video"),
        MultiFieldPanel([
            FieldPanel('image_title'),
            FieldPanel('image_view_all_text'),
            FieldPanel('image_view_all_link'),
            FieldPanel('image_previews'),
        ], heading="Image"),
        MultiFieldPanel([
            FieldPanel('license_title'),
            FieldPanel('license_block'),
        ], heading="License"),
    ]
