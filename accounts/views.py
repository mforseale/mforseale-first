from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from app.models import Rating


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
        'reviews': reviews,
        'ratings': Rating.objects.filter(user=request.user).select_related('movie')  # вот это важно!
    })
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from app.models import List, Movie

@login_required
def create_list(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            List.objects.create(user=request.user, name=name)
    return redirect('profile')

@login_required
def list_detail(request, list_id):
    list_obj = get_object_or_404(List, list_id=list_id, user=request.user)
    if request.method == 'POST':
        # Handle adding/removing movies from the list
        pass
    return render(request, 'list_detail.html', {'list': list_obj})

@login_required
def delete_list(request, list_id):
    list_obj = get_object_or_404(List, list_id=list_id, user=request.user)
    if request.method == 'POST':
        list_obj.delete()
    return redirect('profile')