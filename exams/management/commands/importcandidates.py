# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext as _

from exams.models import import_candidates

class Command(BaseCommand):
    args = '<candidates.xml>'
    help = _('Imports candidates from XML file')

    def handle(self, *args, **options):
        filename = args[0]

        print _("Importing candidates from %(filename)s") % {
            'filename': filename,
        }
        
        imported = import_candidates(filename=filename)

        if type(imported) == dict:
            print _("Import finished! Imported candidates %(candidates_created)d new and %(candidates_updated)d updated, with %(examregistrations)d registrations to exams.") % imported
        else:
            print _("Unknown failure?!")
