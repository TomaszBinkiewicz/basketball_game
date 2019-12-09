from django.core.management.base import BaseCommand
from ._private import create_teams, create_players


class Command(BaseCommand):
    help = 'Populates league with teams and players'

    def handle(self, *args, **options):
        create_teams()
        self.stdout.write(self.style.SUCCESS("Succesfully added teams"))
        create_players()
        self.stdout.write(self.style.SUCCESS("Succesfully created players"))
