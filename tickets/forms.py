from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'priority', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'glass-input',
                'placeholder': 'E.g., Production database timeout or VPN connection error...',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'glass-input',
                'rows': 4,
                'placeholder': 'Provide specific symptoms, reproduction steps, or error logs...',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'glass-input glass-select'
            }),
        }