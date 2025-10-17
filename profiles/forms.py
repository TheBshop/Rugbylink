from django import forms
from django.contrib.auth import get_user_model
from .models import PlayerProfile, TeamProfile, AgentProfile

User = get_user_model()


class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = PlayerProfile
        fields = [
            'profile_picture', 'bio', 'position', 'age', 'location', 
            'height', 'weight', 'availability_status', 'current_team',
            'previous_teams', 'years_playing', 'caps', 'tries', 
            'conversions', 'penalties', 'drop_goals', 'awards',
            'video_urls', 'highlights_url', 'phone', 'social_media'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'previous_teams': forms.Textarea(attrs={'rows': 3}),
            'awards': forms.Textarea(attrs={'rows': 3}),
            'video_urls': forms.Textarea(attrs={'rows': 3}),
            'social_media': forms.Textarea(attrs={'rows': 2}),
            'availability_status': forms.Select(attrs={'class': 'form-select'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].help_text = 'Tell us about yourself, your playing style, and career goals'
        self.fields['previous_teams'].help_text = 'List your previous teams, one per line'
        self.fields['video_urls'].help_text = 'Add links to your highlight videos, one per line'
        self.fields['social_media'].help_text = 'Add links to your social media profiles'


class TeamProfileForm(forms.ModelForm):
    class Meta:
        model = TeamProfile
        fields = [
            'team_name', 'logo', 'description', 'location', 'league', 
            'division', 'website', 'founded_year', 'contact_email',
            'contact_phone', 'stadium', 'capacity', 'social_media'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'social_media': forms.Textarea(attrs={'rows': 2}),
            'league': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].help_text = 'Tell us about your team, history, and what makes you unique'
        self.fields['social_media'].help_text = 'Add links to your team\'s social media profiles'


class AgentProfileForm(forms.ModelForm):
    class Meta:
        model = AgentProfile
        fields = [
            'agency_name', 'profile_picture', 'bio', 'location', 
            'specialization', 'years_experience', 'qualifications',
            'clients', 'phone', 'website', 'social_media', 'services_offered'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'qualifications': forms.Textarea(attrs={'rows': 3}),
            'clients': forms.Textarea(attrs={'rows': 3}),
            'social_media': forms.Textarea(attrs={'rows': 2}),
            'services_offered': forms.Textarea(attrs={'rows': 3}),
            'specialization': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].help_text = 'Tell us about your background and experience in rugby'
        self.fields['qualifications'].help_text = 'List your professional qualifications and certifications'
        self.fields['clients'].help_text = 'Mention notable clients or achievements'
        self.fields['services_offered'].help_text = 'Describe the services you offer to players and teams'

