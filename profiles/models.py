from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

User = get_user_model()


class PlayerProfile(models.Model):
    POSITION_CHOICES = [
        ('LHP', 'Loosehead Prop'),
        ('HKR', 'Hooker'),
        ('THP', 'Tighthead Prop'),
        ('LKR', 'Lock'),
        ('BLF', 'Blindside Flanker'),
        ('OSF', 'Openside Flanker'),
        ('NO8', 'Number 8'),
        ('SCR', 'Scrum Half'),
        ('FLY', 'Fly Half'),
        ('LWC', 'Left Wing Centre'),
        ('ICR', 'Inside Centre'),
        ('OCR', 'Outside Centre'),
        ('RWC', 'Right Wing Centre'),
        ('LWG', 'Left Wing'),
        ('FUB', 'Fullback'),
    ]

    AVAILABILITY_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('UNAVAILABLE', 'Unavailable'),
        ('INJURED', 'Injured'),
        ('RETIRED', 'Retired'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='player_profile')
    profile_picture = models.ImageField(upload_to='profiles/players/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES, blank=True)
    age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(50)], blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    height = models.PositiveIntegerField(help_text="Height in cm", blank=True, null=True)
    weight = models.PositiveIntegerField(help_text="Weight in kg", blank=True, null=True)
    availability_status = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES, default='AVAILABLE')
    
    # Playing History
    current_team = models.CharField(max_length=100, blank=True)
    previous_teams = models.TextField(blank=True, help_text="List previous teams, one per line")
    years_playing = models.PositiveIntegerField(blank=True, null=True)
    
    # Stats and Achievements
    caps = models.PositiveIntegerField(default=0, help_text="Number of international caps")
    tries = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    penalties = models.PositiveIntegerField(default=0)
    drop_goals = models.PositiveIntegerField(default=0)
    awards = models.TextField(blank=True, help_text="List awards and achievements")
    
    # Media
    video_urls = models.TextField(blank=True, help_text="Video URLs, one per line")
    highlights_url = models.URLField(blank=True)
    
    # Contact and Social
    phone = models.CharField(max_length=20, blank=True)
    social_media = models.TextField(blank=True, help_text="Social media links")
    
    # Verification
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"

    def get_absolute_url(self):
        return reverse('profiles:player_detail', kwargs={'pk': self.pk})

    @property
    def total_points(self):
        return (self.tries * 5) + (self.conversions * 2) + (self.penalties * 3) + (self.drop_goals * 3)


class TeamProfile(models.Model):
    LEAGUE_CHOICES = [
        ('PREMIERSHIP', 'Premiership'),
        ('CHAMPIONSHIP', 'Championship'),
        ('NATIONAL_1', 'National 1'),
        ('NATIONAL_2', 'National 2'),
        ('COUNTY', 'County'),
        ('AMATEUR', 'Amateur'),
        ('INTERNATIONAL', 'International'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='team_profile')
    team_name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='profiles/teams/', blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=100)
    league = models.CharField(max_length=20, choices=LEAGUE_CHOICES, blank=True)
    division = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    
    # Contact Information
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    stadium = models.CharField(max_length=100, blank=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    
    # Social Media
    social_media = models.TextField(blank=True, help_text="Social media links")
    
    # Verification
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.team_name

    def get_absolute_url(self):
        return reverse('profiles:team_detail', kwargs={'pk': self.pk})


class AgentProfile(models.Model):
    SPECIALIZATION_CHOICES = [
        ('PLAYERS', 'Player Representation'),
        ('TEAMS', 'Team Management'),
        ('COACHES', 'Coaching Staff'),
        ('RECRUITMENT', 'Recruitment'),
        ('GENERAL', 'General Sports Management'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    agency_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profiles/agents/', blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True)
    location = models.CharField(max_length=100)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES, default='GENERAL')
    
    # Professional Information
    years_experience = models.PositiveIntegerField(blank=True, null=True)
    qualifications = models.TextField(blank=True, help_text="Professional qualifications and certifications")
    clients = models.TextField(blank=True, help_text="Notable clients or achievements")
    
    # Contact Information
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField(blank=True)
    social_media = models.TextField(blank=True, help_text="Social media links")
    
    # Services
    services_offered = models.TextField(blank=True, help_text="Services offered to clients")
    
    # Verification
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.agency_name}"

    def get_absolute_url(self):
        return reverse('profiles:agent_detail', kwargs={'pk': self.pk})


class PlayerHistory(models.Model):
    """Track player's career history with different clubs/teams"""
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='career_history')
    team_name = models.CharField(max_length=100)
    team_type = models.CharField(
        max_length=20,
        choices=[
            ('club', 'Club'),
            ('international', 'International'),
            ('youth', 'Youth/Development'),
            ('academy', 'Academy'),
        ],
        default='club'
    )
    position_played = models.CharField(max_length=3, choices=PlayerProfile.POSITION_CHOICES, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    
    # Performance stats for this period
    appearances = models.PositiveIntegerField(default=0)
    tries_scored = models.PositiveIntegerField(default=0)
    points_scored = models.PositiveIntegerField(default=0)
    
    # Contract details
    contract_type = models.CharField(
        max_length=20,
        choices=[
            ('professional', 'Professional'),
            ('semi_pro', 'Semi-Professional'),
            ('amateur', 'Amateur'),
            ('loan', 'Loan'),
            ('trial', 'Trial'),
        ],
        default='professional'
    )
    
    notes = models.TextField(blank=True, help_text="Additional notes about this period")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_date']
        verbose_name_plural = "Player Histories"
    
    def __str__(self):
        current = " (Current)" if self.is_current else ""
        return f"{self.player.user.get_full_name()} - {self.team_name} ({self.start_date.year}){current}"


class PlayerStats(models.Model):
    """Detailed statistics for players"""
    player = models.OneToOneField(PlayerProfile, on_delete=models.CASCADE, related_name='detailed_stats')
    
    # Physical attributes
    speed_rating = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Speed rating (0-100)"
    )
    strength_rating = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Strength rating (0-100)"
    )
    agility_rating = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Agility rating (0-100)"
    )
    endurance_rating = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Endurance rating (0-100)"
    )
    
    # Technical skills
    passing_accuracy = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Passing accuracy percentage"
    )
    kicking_accuracy = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Kicking accuracy percentage"
    )
    tackling_success = models.PositiveIntegerField(
        default=0, 
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Tackling success percentage"
    )
    
    # Career totals
    total_matches = models.PositiveIntegerField(default=0)
    total_minutes = models.PositiveIntegerField(default=0)
    total_tries = models.PositiveIntegerField(default=0)
    total_assists = models.PositiveIntegerField(default=0)
    total_tackles = models.PositiveIntegerField(default=0)
    total_turnovers = models.PositiveIntegerField(default=0)
    
    # Injury history
    major_injuries = models.TextField(blank=True, help_text="List of major injuries")
    current_injuries = models.TextField(blank=True, help_text="Current injury status")
    
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.player.user.get_full_name()} - Detailed Stats"
    
    @property
    def overall_rating(self):
        """Calculate overall player rating"""
        ratings = [
            self.speed_rating,
            self.strength_rating,
            self.agility_rating,
            self.endurance_rating,
            self.passing_accuracy,
            self.kicking_accuracy,
            self.tackling_success,
        ]
        return sum(ratings) // len(ratings) if ratings else 0