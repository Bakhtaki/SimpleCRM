from django.urls import path
from  .views import (LeadListView,LeadDetailView,LeadUpdateView,LeadCreateView,
                     LeadDeleteView,AssignAgentView,CategoryListView,CategoryDetailView,LeadCategoryUpdateView
                     )

app_name = 'leads'

urlpatterns =[
    path('',LeadListView.as_view(),name='lead_list'),
    path('<int:pk>/',LeadDetailView.as_view(),name='lead_detail'),
    path('<int:pk>/update',LeadUpdateView.as_view(),name='lead_update'),
    path('<int:pk>/assign_agent', AssignAgentView.as_view(), name='assign_agent'),
    path('<int:pk>/delete', LeadDeleteView.as_view(),name='lead_delete'),
    path('create/',LeadCreateView.as_view(),name='lead_create'),
    path('categories/',CategoryListView.as_view(),name='category_list'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category_detail'),
    path('<int:pk>/category', LeadCategoryUpdateView.as_view(), name='lead_category_update'),
]
