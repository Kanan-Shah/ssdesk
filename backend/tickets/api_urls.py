from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    TicketCreateView, TicketListView, TicketDetailView,
    UpdateTicketStatusView, ReopenTicketView, AddCommentView,
    DashboardView, UploadAttachmentView, OverridePriorityView,
    ListCommentsView, ListEventsView,

)
 
# API routes (prefix these with /api/tickets/ in ssdesk/urls.py)
urlpatterns = [
    path('create/',TicketCreateView.as_view(),name='ticket-create'),
    path('',TicketListView.as_view(),name='ticket-list'),
    path('dashboard/',DashboardView.as_view(),name='dashboard-api'),
    path('<int:pk>/',TicketDetailView.as_view(),name='ticket-detail'),
    path('<int:pk>/status/',UpdateTicketStatusView.as_view(),name='update-status'),
    path('<int:pk>/reopen/',ReopenTicketView.as_view(),name='reopen-ticket'),
    path('<int:pk>/comment/',AddCommentView.as_view(),name='add-comment'),
    path('<int:pk>/comments/',ListCommentsView.as_view(),name='list-comments'),
    path('<int:pk>/events/',ListEventsView.as_view(),name='list-events'),
    path('<int:pk>/upload/',UploadAttachmentView.as_view(),name='upload-file'),
    path('<int:pk>/override-priority/', OverridePriorityView.as_view(), name='override-priority'),
]