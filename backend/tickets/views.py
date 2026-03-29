from django.shortcuts import render
from rest_framework import generics
from .models import Ticket,TicketEvent
from .serializers import TicketSerializer
from .services.priority_engine import compute_priority
from .services.sla_engine import compute_sla_deadline

class TicketCreateView(generics.CreateAPIView):
    queryset=Ticket.objects.all()
    serializer_class=TicketSerializer

    def perform_create(self, serializer):
        user=self.request.user
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
