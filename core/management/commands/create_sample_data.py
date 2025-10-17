from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from profiles.models import PlayerProfile, TeamProfile, AgentProfile

User = get_user_model()


class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create sample players
        player1, created = User.objects.get_or_create(
            username='john_doe',
            defaults={
                'email': 'john@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'user_type': 'PLAYER'
            }
        )
        if created:
            player1.set_password('password123')
            player1.save()

        player2, created = User.objects.get_or_create(
            username='jane_smith',
            defaults={
                'email': 'jane@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'user_type': 'PLAYER'
            }
        )
        if created:
            player2.set_password('password123')
            player2.save()

        # Create sample team
        team_user, created = User.objects.get_or_create(
            username='lions_rugby',
            defaults={
                'email': 'info@lionsrugby.com',
                'first_name': 'Lions',
                'last_name': 'Rugby Club',
                'user_type': 'TEAM'
            }
        )
        if created:
            team_user.set_password('password123')
            team_user.save()

        # Create sample agent
        agent_user, created = User.objects.get_or_create(
            username='rugby_agent',
            defaults={
                'email': 'agent@rugbypros.com',
                'first_name': 'Mike',
                'last_name': 'Wilson',
                'user_type': 'AGENT'
            }
        )
        if created:
            agent_user.set_password('password123')
            agent_user.save()

        # Create profiles
        if not hasattr(player1, 'player_profile'):
            PlayerProfile.objects.create(
                user=player1,
                bio='Experienced fly-half with 5 years of professional rugby.',
                position='FLY',
                age=25,
                location='London, UK',
                height=180,
                weight=85,
                current_team='Lions Rugby Club',
                caps=15,
                tries=8,
                conversions=45,
                penalties=12
            )

        if not hasattr(player2, 'player_profile'):
            PlayerProfile.objects.create(
                user=player2,
                bio='Dynamic prop with strong scrummaging skills.',
                position='LHP',
                age=28,
                location='Manchester, UK',
                height=185,
                weight=110,
                current_team='Eagles RFC',
                caps=22,
                tries=2,
                conversions=0,
                penalties=0
            )

        if not hasattr(team_user, 'team_profile'):
            TeamProfile.objects.create(
                user=team_user,
                team_name='Lions Rugby Club',
                description='Premier rugby club with a rich history and strong community presence.',
                location='London, UK',
                league='PREMIERSHIP',
                division='Premiership',
                founded_year=1895,
                contact_email='info@lionsrugby.com'
            )

        if not hasattr(agent_user, 'agent_profile'):
            AgentProfile.objects.create(
                user=agent_user,
                agency_name='Rugby Pros Management',
                bio='Experienced rugby agent helping players advance their careers.',
                location='Birmingham, UK',
                specialization='PLAYERS',
                years_experience=10,
                qualifications='Sports Management Degree, Rugby Union Level 3 Coach'
            )

        self.stdout.write(
            self.style.SUCCESS('Sample data created successfully!')
        )
        self.stdout.write('Sample accounts created:')
        self.stdout.write('- Player: john_doe / password123')
        self.stdout.write('- Player: jane_smith / password123')
        self.stdout.write('- Team: lions_rugby / password123')
        self.stdout.write('- Agent: rugby_agent / password123')

