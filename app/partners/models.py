from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock, RichTextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from app.core.models import LinkOrPageBlock, Partner, PartnerType


# The "partners" and "partner types" snippets are in the core app's models.

class PartnerWithUsPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        
        context['partners'] = Partner.objects.all()
        context['partner_types'] = PartnerType.objects.all()
        return context
    
    max_count = 1
    
    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    header_description = RichTextField(blank=True)

    intro = RichTextField(blank=True)

    partnership_types_title = models.CharField(default="Types of Partnerships")

    meet_our_partners_title = models.CharField(default="Meet Our Partners")
    view_all_partners_text = models.CharField(default="View All Partners")
    view_all_partners_link = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    red_box_title = models.CharField(default="Still have questions?")
    red_box_link_text = models.CharField(default="Contact our team")
    red_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="Become a Partner")
    black_box_link_text = models.CharField(default="Email to partnerships@hotosm.org")
    black_box_link_email = models.EmailField(default="partnerships@hotosm.org", max_length=254)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_description'),
        ], heading="Header"),
        FieldPanel('intro'),
        MultiFieldPanel([
            FieldPanel('partnership_types_title'),
        ], heading="Types of Partnerships"),
        MultiFieldPanel([
            FieldPanel('meet_our_partners_title'),
            FieldPanel('view_all_partners_text'),
            FieldPanel('view_all_partners_link'),
        ], heading="Meet Our Partners"),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_email'),
        ], heading="Dogear Boxes"),
    ]


class OurPartnersPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        partners = Partner.objects.all()
        
        p_types = PartnerType.objects.all()
        query = Q()
        for p_type in p_types:
            if request.GET.get(str(p_type), ''):
                query = query | Q(partner_type__type_name=p_type)
        partners = partners.filter(query).distinct()

        page = request.GET.get('page', 1)
        paginator = Paginator(partners, 12)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            partners = paginator.page(page)
        except PageNotAnInteger:
            partners = paginator.page(1)
        except EmptyPage:
            partners = paginator.page(paginator.num_pages)

        context['partners'] = partners
        context['partner_types'] = p_types
        return context
    
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

    filter_by_type_text = models.CharField(default="Filter by Type")
    
    filter_button_text = models.CharField(default="Submit")

    load_more_partners_text = models.CharField(default="Load More Partners")

    red_box_title = models.CharField(default="Learn ways to partner with HOT")
    red_box_link_text = models.CharField(default="Partner with us")
    red_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)
    black_box_title = models.CharField(default="Become a funding partner")
    black_box_link_text = models.CharField(default="Become a funder")
    black_box_link_url = StreamField(LinkOrPageBlock(), use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('intro'),
        ], heading="Header"),
        FieldPanel('filter_by_type_text'),
        FieldPanel('filter_button_text'),
        FieldPanel('load_more_partners_text'),
        MultiFieldPanel([
            FieldPanel('red_box_title'),
            FieldPanel('red_box_link_text'),
            FieldPanel('red_box_link_url'),
            FieldPanel('black_box_title'),
            FieldPanel('black_box_link_text'),
            FieldPanel('black_box_link_url'),
        ], heading="Dogear Boxes"),
    ]
