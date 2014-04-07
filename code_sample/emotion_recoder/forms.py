from django import forms

from .models import Emotions


class EmotionForm(forms.ModelForm):
    """Form for Emotions models"""
    
    description = forms.CharField(max_length=255, widget=forms.Textarea)
    
    class Meta:
        model = Emotions
        fields = ("description",)