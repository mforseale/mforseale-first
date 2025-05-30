from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
from app.models import Review  # путь к модели Review

@login_required
def profile_view(request):
    reviews = Review.objects.filter(user=request.user).select_related('movie')
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'reviews': reviews
    })