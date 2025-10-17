from django.contrib import admin
from .models import PlayerProfile, TeamProfile, AgentProfile


@admin.register(PlayerProfile)
class PlayerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'position', 'age', 'location', 'availability_status', 'is_verified')
    list_filter = ('position', 'availability_status', 'is_verified', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'profile_picture', 'bio', 'position', 'age', 'location', 'height', 'weight')
        }),
        ('Playing Info', {
            'fields': ('availability_status', 'current_team', 'previous_teams', 'years_playing')
        }),
        ('Stats', {
            'fields': ('caps', 'tries', 'conversions', 'penalties', 'drop_goals', 'awards')
        }),
        ('Media', {
            'fields': ('video_urls', 'highlights_url')
        }),
        ('Contact', {
            'fields': ('phone', 'social_media')
        }),
        ('Verification', {
            'fields': ('is_verified', 'created_at', 'updated_at')
        }),
    )


@admin.register(TeamProfile)
class TeamProfileAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'location', 'league', 'division', 'is_verified')
    list_filter = ('league', 'division', 'is_verified', 'created_at')
    search_fields = ('team_name', 'location', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'team_name', 'logo', 'description', 'location')
        }),
        ('League Info', {
            'fields': ('league', 'division', 'founded_year')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone', 'website', 'social_media')
        }),
        ('Stadium', {
            'fields': ('stadium', 'capacity')
        }),
        ('Verification', {
            'fields': ('is_verified', 'created_at', 'updated_at')
        }),
    )


@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'agency_name', 'location', 'specialization', 'is_verified')
    list_filter = ('specialization', 'is_verified', 'created_at')
    search_fields = ('user__username', 'agency_name', 'location')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'agency_name', 'profile_picture', 'bio', 'location', 'specialization')
        }),
        ('Professional Info', {
            'fields': ('years_experience', 'qualifications', 'clients', 'services_offered')
        }),
        ('Contact', {
            'fields': ('phone', 'website', 'social_media')
        }),
        ('Verification', {
            'fields': ('is_verified', 'created_at', 'updated_at')
        }),
    )