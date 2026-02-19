from django.core.management.base import BaseCommand
from medicines.models import Manufacturer, Formula, Medicine

class Command(BaseCommand):
    help = "Seed initial data for medicines app"

    def handle(self, *args, **kwargs):

        # Manufacturers
        pfizer, _ = Manufacturer.objects.get_or_create(
            name="Pfizer",
            defaults={"address": "New York, USA"}
        )

        novartis, _ = Manufacturer.objects.get_or_create(
            name="Novartis",
            defaults={"address": "Basel, Switzerland"}
        )

        # Formulas
        formula1, _ = Formula.objects.get_or_create(
            composition="Paracetamol 500mg",
            defaults={"dosage": "1 tablet every 6 hours"}
        )

        formula2, _ = Formula.objects.get_or_create(
            composition="Ibuprofen 400mg",
            defaults={"dosage": "1 tablet every 8 hours"}
        )

        # Medicines
        Medicine.objects.get_or_create(
            name="Panadol",
            manufacturer=pfizer,
            formula=formula1,
            defaults={"description": "Used for fever and mild pain"}
        )

        Medicine.objects.get_or_create(
            name="Brufen",
            manufacturer=novartis,
            formula=formula2,
            defaults={"description": "Used for inflammation and pain relief"}
        )

        self.stdout.write(self.style.SUCCESS("Seed data inserted successfully!"))