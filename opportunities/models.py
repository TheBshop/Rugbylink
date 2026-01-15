from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.urls import reverse

User = get_user_model()


class ContractOpportunity(models.Model):
    CONTRACT_TYPE_CHOICES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('SEASONAL', 'Seasonal'),
        ('TRIAL', 'Trial'),
        ('ACADEMY', 'Academy'),
        ('SENIOR', 'Senior'),
        ('JUNIOR', 'Junior'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
        ('PAUSED', 'Paused'),
        ('FILLED', 'Filled'),
    ]

    team = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_opportunities', limit_choices_to={'user_type': 'TEAM'})
    title = models.CharField(max_length=200)
    position = models.CharField(max_length=100, help_text="Rugby position (e.g., Fly Half, Prop, etc.)")
    description = models.TextField(max_length=2000)
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])
    location = models.CharField(max_length=100)
    requirements = models.TextField(max_length=1000, help_text="Required skills, experience, and qualifications")
    benefits = models.TextField(max_length=1000, blank=True, help_text="Additional benefits and perks")
    
    # Dates
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    
    # Status
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Additional Info
    is_featured = models.BooleanField(default=False)
    applications_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-posted_date']
        verbose_name_plural = "Contract Opportunities"

    def __str__(self):
        return f"{self.team.team_profile.team_name if hasattr(self.team, 'team_profile') else self.team.username}: {self.title}"

    def get_absolute_url(self):
        return reverse('opportunities:detail', kwargs={'pk': self.pk})

    def update_applications_count(self):
        self.applications_count = self.applications.count()
        self.save(update_fields=['applications_count'])

    @property
    def salary_range(self):
        if self.salary_min and self.salary_max:
            return f"£{self.salary_min:,.0f} - £{self.salary_max:,.0f}"
        elif self.salary_min:
            return f"£{self.salary_min:,.0f}+"
        elif self.salary_max:
            return f"Up to £{self.salary_max:,.0f}"
        return "Salary not specified"


class Application(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('REVIEWED', 'Under Review'),
        ('SHORTLISTED', 'Shortlisted'),
        ('INTERVIEWED', 'Interviewed'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('WITHDRAWN', 'Withdrawn'),
    ]

    opportunity = models.ForeignKey(ContractOpportunity, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', limit_choices_to={'user_type': 'PLAYER'})
    cover_letter = models.TextField(max_length=2000, help_text="Tell us why you're interested in this opportunity")
    cv_document = models.FileField(upload_to='applications/cvs/', blank=True, null=True)
    additional_info = models.TextField(max_length=1000, blank=True, help_text="Any additional information you'd like to share")
    
    # Status and dates
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    applied_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Team notes
    team_notes = models.TextField(max_length=1000, blank=True, help_text="Internal notes for the team")
    
    class Meta:
        unique_together = ['opportunity', 'applicant']
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.applicant.username} applied for {self.opportunity.title}"

    def get_absolute_url(self):
        return reverse('opportunities:application_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.opportunity.update_applications_count()


class ExternalOpportunity(models.Model):
    class SportChoices(models.TextChoices):
        ARCHERY = "ARCHERY", "Archery"
        ATHLETICS = "ATHLETICS", "Athletics"
        BADMINTON = "BADMINTON", "Badminton"
        BASEBALL = "BASEBALL", "Baseball"
        BASKETBALL = "BASKETBALL", "Basketball"
        BOXING = "BOXING", "Boxing"
        CANOEING = "CANOEING", "Canoeing"
        CYCLING = "CYCLING", "Cycling"
        FENCING = "FENCING", "Fencing"
        FIGURE_SKATING = "FIGURE_SKATING", "Figure Skating"
        FOOTBALL = "FOOTBALL", "Football"
        GOLF = "GOLF", "Golf"
        GYMNASTICS = "GYMNASTICS", "Gymnastics"
        HANDBALL = "HANDBALL", "Handball"
        HOCKEY = "HOCKEY", "Hockey"
        JUDO = "JUDO", "Judo"
        KARATE = "KARATE", "Karate"
        ROWING = "ROWING", "Rowing"
        RUGBY = "RUGBY", "Rugby"
        SAILING = "SAILING", "Sailing"
        SKATING = "SKATING", "Skating"
        SKIING = "SKIING", "Skiing"
        SOFTBALL = "SOFTBALL", "Softball"
        SURFING = "SURFING", "Surfing"
        SWIMMING = "SWIMMING", "Swimming"
        SYNCHRONIZED_SWIMMING = "SYNCHRONIZED_SWIMMING", "Synchronized Swimming"
        TABLE_TENNIS = "TABLE_TENNIS", "Table Tennis"
        TAEKWONDO = "TAEKWONDO", "Taekwondo"
        TENNIS = "TENNIS", "Tennis"
        TRIATHLON = "TRIATHLON", "Triathlon"
        VOLLEYBALL = "VOLLEYBALL", "Volleyball"
        WEIGHTLIFTING = "WEIGHTLIFTING", "Weightlifting"

    class LevelChoices(models.TextChoices):
        PROFESSIONAL = "PROFESSIONAL", "Professional"
        SEMI_PRO = "SEMI_PRO", "Semi-Pro"
        SCOUTING = "SCOUTING", "Scouting"
        COLLEGE = "COLLEGE", "College"
        UNIVERSITY_SCHOLARSHIP = "UNIVERSITY_SCHOLARSHIP", "University Scholarship"
        YOUTH_CAMP = "YOUTH_CAMP", "Youth Camp"
        TRYOUT = "TRYOUT", "Tryout"
        PART_TIME = "PART_TIME", "Part Time"

    class GenderChoices(models.TextChoices):
        MEN = "MEN", "Men"
        WOMEN = "WOMEN", "Women"
        COED = "COED", "Coed"

    title = models.CharField(max_length=255)
    sport = models.CharField(max_length=40, choices=SportChoices.choices)
    level = models.CharField(max_length=40, choices=LevelChoices.choices)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    country = models.CharField(max_length=100)
    deadline = models.DateField(blank=True, null=True)
    link = models.URLField(max_length=500)
    source = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    scraped_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sport", "level", "gender", "country", "deadline", "title"]
        verbose_name = "External Opportunity"
        verbose_name_plural = "External Opportunities"

    def __str__(self):
        return f"{self.title} ({self.get_sport_display()})"
