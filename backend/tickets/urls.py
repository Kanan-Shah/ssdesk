from django.urls import path
from .views import TicketCreateView, TicketListView

urlpatterns=[
    path("create/",TicketCreateView.as_view(),name="ticket-create"),
    path("",TicketListView.as_view(),name="ticket-list"),
]