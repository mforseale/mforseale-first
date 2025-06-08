# forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Напишите отзыв...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 10}),
        }
# forms.py
from django import forms
from .models import UserProfile, Movie

class UserProfileForm(forms.ModelForm):
    favorite_movies = forms.ModelMultipleChoiceField(
        queryset=Movie.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'favorite_movies']
from django import forms
from .models import Rating

from django import forms

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score']
        widgets = {
            'score': forms.NumberInput(attrs={'min': 1, 'max': 10, 'type': 'number'})
        }


