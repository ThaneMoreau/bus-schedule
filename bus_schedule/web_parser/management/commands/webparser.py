from django.core.management.base import BaseCommand
from web_parser.utils.webparser import webparser


class Command(BaseCommand):
    def handle(self, **options):
        webparser.run()
