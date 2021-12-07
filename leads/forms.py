from django import forms
from django.contrib.auth import get_user_model
from django.http import request
from .models import Lead, User,Agent,Category
from django.contrib.auth.forms import UserCreationForm, UsernameField

User = get_user_model()


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields =(
            "first_name",
            "last_name",
            "age",
            "agent",
            "email",
            "phone_number",
            'description'
        )

class LeadForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    age = forms.IntegerField(min_value=0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)
        fields_classes = { "username": UsernameField}

class AssignAgentForm(forms.Form):
    agent  = forms.ModelChoiceField(queryset=Agent.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request')
        agents = Agent.objects.filter(organization =request.user.userprofile)
        super(AssignAgentForm, self).__init__(*args, **kwargs)
        self.fields['agent'].queryset =agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            "category",
        )
