from django.contrib import admin

from opportunities.models import Application, ContractOpportunity, ExternalOpportunity


@admin.register(ContractOpportunity)
class ContractOpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "team", "location", "contract_type", "status", "posted_date")
    list_filter = ("contract_type", "status", "location")
    search_fields = ("title", "team__username", "location", "position")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("opportunity", "applicant", "status", "applied_date")
    list_filter = ("status",)
    search_fields = ("opportunity__title", "applicant__username")


@admin.register(ExternalOpportunity)
class ExternalOpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "sport", "level", "gender", "country", "deadline", "is_active")
    list_filter = ("sport", "level", "gender", "country", "is_active")
    search_fields = ("title", "country", "source", "link")
