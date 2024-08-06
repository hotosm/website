from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.blocks import StreamBlock, CharBlock, URLBlock, RichTextBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from app.projects.models import IndividualProjectPage
from app.core.models import LinkOrPageBlock


class UseCaseStructBlock(StructBlock):
    description = RichTextBlock()
    link_text = CharBlock()
    link = LinkOrPageBlock(blank=True, null=True)


class UseCaseBlock(StreamBlock):
    blocks = UseCaseStructBlock()


class IndividualImpactAreaPage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        projects_list = IndividualProjectPage.objects.live().filter(
            Q(impact_area_list__contains=[{'type': 'impact_area', 'value': context['page'].id}])
        ).filter(locale=context['page'].locale)
        page = request.GET.get('page', 1)
        paginator = Paginator(projects_list, 8)  # if you want more/less items per page (i.e., per load), change the number here to something else
        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)
        
        context['projects'] = projects
        other_impact_areas = IndividualImpactAreaPage.objects.live().filter(locale=context['page'].locale)
        context['other_impact_areas'] = other_impact_areas
        return context

    parent_page_types = [
        'impact_areas.ImpactAreasPage'
    ]

    header_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    header_text = RichTextField(blank=True)
    
    external_icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="The icon representing this page which is shown for previews of this page on other pages. This should be a purely black image which is ideally as wide as it is tall."
    )
    intro = RichTextField(blank=True, help_text="This text will not be shown on the page itself, and will instead be shown as the short description for the page for instances such as the Search page or the Impact Areas page.")
    
    intro_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Intro image"
    )
    description = RichTextField(blank=True)

    use_cases = StreamField(UseCaseBlock(), use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('header_image'),
            FieldPanel('header_text'),
        ], heading="Header"),
        MultiFieldPanel([
            FieldPanel('external_icon'),
            FieldPanel('intro'),
        ], heading="External"),
        MultiFieldPanel([
            FieldPanel('intro_image'),
            FieldPanel('description'),
        ], heading="Body"),
        MultiFieldPanel([
            FieldPanel('use_cases'),
        ], heading="Use Cases"),
    ]


class ImpactAreasPage(Page):
    max_count = 1
    
    subpage_types = [
        'impact_areas.IndividualImpactAreaPage'
    ]

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Header image"
    )
    header_text = RichTextField(blank=True)
    
    intro = RichTextField(blank=True)
    description = RichTextField(blank=True)

    # > IMPACT AREA SHARED FIELDS
    use_cases_title = models.CharField(default="Use Cases")

    projects_title = models.CharField(default="Projects")
    view_all_projects_text = models.CharField(default="View all projects")
    view_all_projects_link = models.URLField(blank=True)
    load_more_projects_text = models.CharField(default="Load More Projects")

    explore_impact_areas_text = models.CharField(default="Explore Other Impact Areas")

    red_dogear_box_title = models.CharField(default="Learn more about Tools & Resources and Data Access")
    red_dogear_box_link_text = models.CharField(default="View Tools & Resources")
    red_dogear_box_link_url = models.URLField(blank=True)

    black_dogear_box_title = models.CharField(default="Check many opportunities to get involved with HOT!")
    black_dogear_box_link_text = models.CharField(default="Get Involved with HOT")
    black_dogear_box_link_url = models.URLField(blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('image'),
            FieldPanel('header_text'),
        ], heading="Header section"),
        FieldPanel('intro'),
        FieldPanel('description'),
        MultiFieldPanel([
            MultiFieldPanel([
                FieldPanel('use_cases_title'),
            ], heading="Use Cases"),
            MultiFieldPanel([
                FieldPanel('projects_title'),
                FieldPanel('view_all_projects_text'),
                FieldPanel('view_all_projects_link'),
                FieldPanel('load_more_projects_text'),
            ], heading="Projects"),
            FieldPanel('explore_impact_areas_text'),
            MultiFieldPanel([
                FieldPanel('red_dogear_box_title'),
                FieldPanel('red_dogear_box_link_text'),
                FieldPanel('red_dogear_box_link_url'),
                FieldPanel('black_dogear_box_title'),
                FieldPanel('black_dogear_box_link_text'),
                FieldPanel('black_dogear_box_link_url'),
            ], heading="Dogear Boxes"),
        ], heading="Impact Area Shared Fields"),
    ]
