from django.shortcuts import render
from django.views.generic import TemplateView

class OpportunityListView(TemplateView):
    template_name = 'opportunities/list.html'

class OpportunityDetailView(TemplateView):
    template_name = 'opportunities/detail.html'

class OpportunityCreateView(TemplateView):
    template_name = 'opportunities/create.html'

class OpportunityUpdateView(TemplateView):
    template_name = 'opportunities/edit.html'

class MyOpportunitiesView(TemplateView):
    template_name = 'opportunities/my_opportunities.html'

class MyApplicationsView(TemplateView):
    template_name = 'opportunities/my_applications.html'

class ApplicationCreateView(TemplateView):
    template_name = 'opportunities/apply.html'

class ApplicationDetailView(TemplateView):
    template_name = 'opportunities/application_detail.html'