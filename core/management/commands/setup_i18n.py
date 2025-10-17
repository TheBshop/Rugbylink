from django.core.management.base import BaseCommand
import os
import shutil
from pathlib import Path


class Command(BaseCommand):
    help = 'Setup internationalization files for RugbyLink'

    def handle(self, *args, **options):
        self.stdout.write('Setting up internationalization...')
        
        # Create basic .mo files from .po files
        languages = ['es', 'fr', 'it', 'pt']
        
        for lang in languages:
            po_file = Path(f'locale/{lang}/LC_MESSAGES/django.po')
            mo_file = Path(f'locale/{lang}/LC_MESSAGES/django.mo')
            
            if po_file.exists():
                # Copy .po to .mo (basic setup without gettext)
                shutil.copy(po_file, mo_file)
                self.stdout.write(f'✓ Created {mo_file}')
            else:
                self.stdout.write(f'⚠ {po_file} not found')
        
        self.stdout.write(
            self.style.SUCCESS('Internationalization setup complete!')
        )
        self.stdout.write('Note: For production, install GNU gettext tools and use:')
        self.stdout.write('  python manage.py compilemessages')

