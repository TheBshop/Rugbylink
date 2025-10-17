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