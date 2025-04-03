from django.db import transaction

from django.core.management.base import BaseCommand
from app.projects.models import IndividualProjectPage
from app.core.models import Partner


def remigrate_project_partners():
    projects = IndividualProjectPage.objects.all().filter(locale=1)

    for project in projects:
        partners = []
        for partner in project.partner_list:
            if partner.block_type == "partner":
                partners += [{"type": "partner", "value": partner.value.id}]
                continue
            
            results = Partner.objects.all().filter(partner_name=str(partner.value))
            if not results:
                partners += [{"type": "manual_partner", "value": partner.value}]
                continue

            partners += [{"type": "partner", "value": results[0].id}]
        
        project.partner_list = partners
        
        with transaction.atomic():
            project.save()


class Command(BaseCommand):
    help = "Migrates projects"

    def handle(self, *args, **options):
        self.stdout.write("i'm testing! i'm testing!")

        remigrate_project_partners()