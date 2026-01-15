import csv
from datetime import date
from typing import Optional

from django.core.management.base import BaseCommand, CommandError

from opportunities.models import ExternalOpportunity


class Command(BaseCommand):
    help = "Export external opportunities to a CSV file."

    def add_arguments(self, parser):
        parser.add_argument(
            "--deadline-after",
            type=str,
            default=None,
            help="Filter opportunities with deadline on/after this date (YYYY-MM-DD).",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=100,
            help="Maximum number of rows to export.",
        )
        parser.add_argument(
            "--output",
            type=str,
            default=None,
            help="Path to output CSV file. Defaults to stdout.",
        )
        parser.add_argument(
            "--include-inactive",
            action="store_true",
            help="Include inactive opportunities in the export.",
        )

    def handle(self, *args, **options):
        deadline_after = self._parse_deadline(options["deadline_after"])
        opportunities = ExternalOpportunity.objects.all()
        if not options["include_inactive"]:
            opportunities = opportunities.filter(is_active=True)
        if deadline_after:
            opportunities = opportunities.filter(deadline__gte=deadline_after)
        opportunities = opportunities.order_by(
            "sport",
            "level",
            "gender",
            "country",
            "deadline",
            "title",
        )
        if options["limit"]:
            opportunities = opportunities[: options["limit"]]

        rows = [
            {
                "title": opportunity.title,
                "sport": opportunity.get_sport_display(),
                "level": opportunity.get_level_display(),
                "gender": opportunity.get_gender_display(),
                "country": opportunity.country,
                "deadline": opportunity.deadline.isoformat() if opportunity.deadline else "",
                "link": opportunity.link,
                "source": opportunity.source,
                "scraped_at": opportunity.scraped_at.isoformat(),
            }
            for opportunity in opportunities
        ]

        fieldnames = [
            "title",
            "sport",
            "level",
            "gender",
            "country",
            "deadline",
            "link",
            "source",
            "scraped_at",
        ]

        if options["output"]:
            with open(options["output"], "w", encoding="utf-8", newline="") as csv_file:
                self._write_rows(csv_file, fieldnames, rows)
            self.stdout.write(self.style.SUCCESS(f"Exported {len(rows)} rows."))
            return

        self._write_rows(self.stdout, fieldnames, rows)

    def _parse_deadline(self, raw_value: Optional[str]) -> Optional[date]:
        if not raw_value:
            return None
        try:
            return date.fromisoformat(raw_value)
        except ValueError as exc:
            raise CommandError("--deadline-after must be in YYYY-MM-DD format.") from exc

    def _write_rows(self, output, fieldnames, rows):
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
