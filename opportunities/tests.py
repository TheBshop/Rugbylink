import io

from django.core.management import call_command
from django.test import TestCase

from opportunities.models import ExternalOpportunity


class ExportExternalOffersCsvTests(TestCase):
    def test_exports_active_offers_with_deadline_filter(self):
        ExternalOpportunity.objects.create(
            title="National Tryout Camp",
            sport=ExternalOpportunity.SportChoices.RUGBY,
            level=ExternalOpportunity.LevelChoices.TRYOUT,
            gender=ExternalOpportunity.GenderChoices.MEN,
            country="USA",
            deadline="2026-02-01",
            link="https://example.com/tryouts/1",
            source="Example Source",
            is_active=True,
        )
        ExternalOpportunity.objects.create(
            title="Closed Camp",
            sport=ExternalOpportunity.SportChoices.RUGBY,
            level=ExternalOpportunity.LevelChoices.TRYOUT,
            gender=ExternalOpportunity.GenderChoices.MEN,
            country="USA",
            deadline="2025-12-01",
            link="https://example.com/tryouts/old",
            source="Example Source",
            is_active=True,
        )

        output = io.StringIO()

        call_command(
            "export_external_offers_csv",
            "--deadline-after",
            "2026-01-15",
            stdout=output,
        )

        csv_output = output.getvalue().strip().splitlines()
        self.assertEqual(
            csv_output[0],
            "title,sport,level,gender,country,deadline,link,source,scraped_at",
        )
        self.assertEqual(len(csv_output), 2)
        self.assertIn("National Tryout Camp,Rugby,Tryout,Men,USA,2026-02-01", csv_output[1])
