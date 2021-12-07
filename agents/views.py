import random
from django.shortcuts import render ,reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from leads.models import Agent ,UserProfile,User
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail

# Create your views here.


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"


    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agent_create.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent_list')


    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer =False
        user.set_password(f"{random.randint(0,1000000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organization=self.request.user.userprofile
            )
        send_mail(
            subject='You are invited to be an agent',
            message='You were added as an agent on SimpleCRM.Please login to See Your assigned leads',
            from_email ='admin@simplecrm.local',
            recipient_list= [user.email]
        )
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_detail.html'
    context_object_name = "agent"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return  Agent.objects.filter(organization = organization)


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agent_update.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agent_list')

    def get_queryset(self):
        organization = self.request.user.userprofile
        return  Agent.objects.filter(organization=organization)


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agent_delete.html'
    context_object_name = "agent"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return  Agent.objects.filter(organization = organization)

    def get_success_url(self):
        return reverse('agents:agent_list')