# pylint: disable=missing-module-docstring
from django.db.models.query import QuerySet
from django.core.mail import send_mail
from django.shortcuts import render ,redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, request
from django.views import generic
from .models import Category, Lead , Agent ,User
from .forms import  LeadForm , LeadModelForm ,CustomUserCreationForm ,AssignAgentForm ,LeadCategoryUpdateForm
from agents.mixins import OrganizerAndLoginRequiredMixin




# Create your views here.

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name ="landing.html"

def landing_Page(request):
    return render(request,'landing.html')


class LeadListView(LoginRequiredMixin,generic.ListView):
    template_name = 'leads/lead_list.html'
    context_object_name = 'leads'

    def get_queryset(self):
        user = self.request.user

        #initial queryset  of lead list for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization =user.userprofile,agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization =user.agent.organization,agent__isnull=False)
            #filter for the agent that is logged in
            queryset =queryset.filter(agent__user = user)

        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Lead.objects.filter(organization =user.userprofile,agent__isnull=True)
            context.update({
                "unassigned_leads" : queryset
            })
        return context

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        'leads': leads
    }
    return render(request, 'leads/lead_list.html', context)


class LeadDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = 'leads/lead_detail.html'
    context_object_name = 'lead'

    def get_queryset(self):
        user = self.request.user
        #initial queryset  of lead list for the entire organization

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        'lead': lead
    }
    return render(request, 'leads/lead_detail.html', context)


class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/lead_create.html'
    form_class =LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead_list")

    def form_valid(self, form):
        """
        Send an Email when Lead Creates
        """
        lead = form.save(commit=False)
        lead.organization =self.request.user.userprofile
        lead.save()
        # Send Email
        send_mail(
            subject = "A New Lead has been created",
            message = "Please check the website for new lead",
            from_email = "test@test.com",
            recipient_list = ['test2@test.com']
        )
        return super(LeadCreateView, self).form_valid(form)


def lead_create(request):
    form = LeadModelForm()
    if request.method == 'POST':
        print("Receiving data")
        form = LeadModelForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = form.cleaned_data['agent']
            form.save()
            return redirect('/leads')
    context = {
        'form': form
    }
    return render(request, 'leads/lead_create.html', context)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/lead_update.html'
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        #initial queryset  of lead list for the entire organization
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead_list")


def lead_update(request,pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance = lead)
    if request.method == 'POST':
        form = LeadModelForm(request.POST,instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context ={
        'form' : form ,
        'lead' : lead
    }
    return render(request, 'leads/lead_update.html',context)


class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/lead_delete.html'

    def get_queryset(self):
        user = self.request.user
        #initial queryset  of lead list for the entire organization
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead_list")

def lead_delete(request,pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('/leads')



class AssignAgentView(OrganizerAndLoginRequiredMixin,generic.FormView):
    template_name ="leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self,**kwargs):
        kwargs = super(AssignAgentView,self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead_list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead =Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView,self).form_valid(form)


class CategoryListView(LoginRequiredMixin,generic.ListView):
    template_name = 'leads/category_list.html'
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(CategoryListView, self).get_context_data(**kwargs)

        #initial queryset  of lead list for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization =user.userprofile)
        else:
            queryset = Lead.objects.filter(organization = user.agent.organization)
        context.update({
            "unassigned_leads_count" : queryset.filter(category__isnull=True).count()
        })

        return context

    def get_queryset(self):
        user = self.request.user

        #initial queryset  of lead list for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization =user.agent.organization)
            #filter for the agent that is logged in
        return queryset

class CategoryDetailView(LoginRequiredMixin,generic.DetailView):
    template_name ="leads/category_detail.html"
    context_object_name = "category"



    def get_queryset(self):
        user = self.request.user

        #initial queryset  of lead list for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(
                organization=user.agent.organization)
            #filter for the agent that is logged in
        return queryset

class LeadCategoryUpdateView(LoginRequiredMixin,generic.UpdateView):
    template_name = 'leads/lead_category_update.html'
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization)
            #filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead_detail", kwargs={"pk" :self.get_object().id})
