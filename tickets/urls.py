from django.urls import path
from . import views

urlpatterns = [
    path('', views.portal_home, name='portal_home'),
    path('tickets/<int:ticket_id>/status/', views.update_status, name='update_status'),
]
