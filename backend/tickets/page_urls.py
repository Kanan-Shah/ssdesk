from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (

    ticket_list_page, ticket_create_page, ticket_detail_page, dashboard_page, signup_page
)
# Page (template) routes — prefix with /tickets/ in ssdesk/urls.py
urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/login/'),name='logout'),
    path('signup/',signup_page,name='signup'),
    path('',ticket_list_page,name='ticket-list-page'),
    path('create/',ticket_create_page,name='ticket-create-page'),
    path('dashboard/',dashboard_page,name='dashboard-page'),
    path('<int:pk>/',ticket_detail_page,name='ticket-detail-page'),
]