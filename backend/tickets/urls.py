from django.urls import path
from .views import TicketCreateView, TicketListView,TicketDetailView,UpdateTicketStatusView,ReopenTicketView,AddCommentView,DashboardView

urlpatterns=[
    path("create/",TicketCreateView.as_view(),name="ticket-create"),
    path("",TicketListView.as_view(),name="ticket-list"),
    path("<int:pk>/",TicketDetailView().as_view(),name="ticket-detail"),
    path("<int:pk>/status/",UpdateTicketStatusView.as_view(),name="update-status"),
    path("<int:pk>/reopen/",ReopenTicketView.as_view(),name="reopen-ticket"),
    path("<int:pk>/comment/",AddCommentView.as_view(),name="add-comment"),
    path("dashboard/",DashboardView.as_view(),name="dashboard"),
]