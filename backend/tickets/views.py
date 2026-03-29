from django.shortcuts import render
from rest_framework import generics

from django.utils import timezone
from .models import Ticket,TicketEvent
from .serializers import TicketSerializer
from .services.priority_engine import compute_priority
from .services.sla_engine import compute_sla_deadline
from django.contrib.auth.models import User

class TicketCreateView(generics.CreateAPIView):
    queryset=Ticket.objects.all()
    serializer_class=TicketSerializer

    def perform_create(self, serializer):
        user=self.request.user
        if user.is_anonymous:
            user=User.objects.first()
        impact=serializer.validated_data.get("impact")
        urgency=serializer.validated_data.get("urgency")
        category=serializer.validated_data.get("category")
        description=serializer.validated_data.get("description")

        #Step 1: Compute priority
        priority=compute_priority(
            impact=impact,
            urgency=urgency,
            category=category,
            description=description,
            reopen_count=0
        )
        # step 2 : compute sla
        sla_deadline=compute_sla_deadline(priority)

        #step 3: Save Ticket
        ticket=serializer.save(
            created_by=user,
            priority=priority,
            sla_deadline=sla_deadline,
            status="OPEN"
        )

        #step 4: Create events
        TicketEvent.objects.create(
            ticket=ticket,
            event_type="TICKET_CREATED"
        )

        TicketEvent.objects.create(
            ticket=ticket,
            event_type="PRIORITY_COMPUTED",
            metadata={"priority":priority}
        )

class TicketListView(generics.ListAPIView):
    serializer_class=TicketSerializer

    def get_queryset(self):
        user=self.request.user
        if user.is_anonymous:
            user=User.objects.first()
        queryset=Ticket.objects.all()

        #role based filtering
        if not user.is_staff:
            queryset=queryset.filter(created_by=user)

        # Filters
        status=self.request.query_params.get("status")
        category=self.request.query_params.get("category")
        priority=self.request.query_params.get("priority")
        overdue=self.request.query_params.get("overdue")

        if status:
            queryset=queryset.filter(status=status)
        if category:
            queryset=queryset.filter(category=category)
        if priority:
            queryset=queryset.filter(priority=priority)
        if overdue==True:
            queryset=queryset.filter(sla_deadline__lt=timezone.now())
        
        #Sorting
        sort_by=self.request.query_params.get("sort")

        if sort_by=="latest":
            queryset=queryset.order_by("-created_at")
        elif sort_by=="oldest":
            queryset=queryset.order_by("-created_at")
        elif sort_by=="priority":
            # custom ordering - P0 highest priority
            queryset=queryset.extra(
                select={
                    "priority_order":"""
                    CASE
                        WHEN priority='P0' THEN 1
                        WHEN priority='P1' THEN 2
                        WHEN priority='P2' THEN 3
                        WHEN priority='P3' THEN 4
                    END
                    """
                }
            ).order_by("priority_order")
        return queryset
        