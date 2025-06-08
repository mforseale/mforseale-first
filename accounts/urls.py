from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='signup'), name='logout'),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('lists/create/', views.create_list, name='create_list'),
    path('lists/<int:list_id>/', views.list_detail, name='list_detail'),
    path('lists/<int:list_id>/delete/', views.delete_list, name='delete_list'),
]