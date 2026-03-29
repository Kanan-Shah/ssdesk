from django.shortcuts import render
from rest_framework import generics
from django.utils import timezone
from .models import Ticket,TicketEvent,Comment,Attachment
from .serializers import TicketSerializer
from .services.priority_engine import compute_priority
from .services.sla_engine import compute_sla_deadline
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count,Avg,F,ExpressionWrapper,DurationField
from datetime import timedelta
from rest_framework.parsers import MultiPartParser,FormParser

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

class TicketDetailView(generics.RetrieveAPIView):

    serializer_class=TicketSerializer
    def get_queryset(self):
        user=self.request.user
        queryset=Ticket.objects.all()

        if not user.is_staff:
            queryset=queryset.filter(created_by=user)
        return queryset

VALID_TRANSITIONS={
    "OPEN":["IN_PROGRESS"],
    "IN_PROGRESS":["RESOLVED"],
    "RESOLVED":["CLOSED"],
    "CLOSED":[]
}       

class UpdateTicketStatusView(APIView):
    def post(self,request,pk):
        try:
            ticket=Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error":"Ticket not found"},status=404)
        new_status=request.data.get("status")

        if new_status not in VALID_TRANSITIONS.get(ticket.status,[]):
            return Response(
                {"error":"Invalid status transition"},
                status=400
            )
        old_status=ticket.status
        ticket.status=new_status
        ticket.save()

        #event log
        TicketEvent.objects.create(
            ticket=ticket,
            event_type="STATUS_CHANGED",
            metadata={"from":old_status, "to":new_status}
        )

        return Response({"message":"Status updated successfully"})

class ReopenTicketView(APIView):
    def post(self,request,pk):
        try:
            ticket=Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error":"Ticket not found"},status=404)
        if ticket.status!="CLOSED":
            return Response({"error":"only closed tickets can be reopened"}),
        reason=request.data.get("reason")

        ticket.status="OPEN"
        ticket.reopen_count+=1

        #recompute priority
        from .services.priority_engine import compute_priority
        from .services.sla_engine import compute_sla_deadline
        ticket.priority=compute_priority(
            ticket.impact,
            ticket.urgency,
            ticket.category,
            ticket.description,
            ticket.reopen_count
        )
        ticket.sla_deadline=compute_sla_deadline(ticket.priority)

        ticket.save()

        TicketEvent.objects.create(
            ticket=ticket,
            event_type="TICKET_REOPENED",
            metadata={"reason":reason}
        )
        return Response({"message":"Ticket reopened"})

class AddCommentView(APIView):
    def post(self,request,pk):
        try:
            ticket=Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error":"Ticket not found"},status=404)
        
        user=request.user
        if user.is_anonymous:
            from django.contrib.auth.models import User
            user=User.objects.first()
        content=request.data.get("content")
        comment_type=request.data.get("type","PUBLIC")

        comment=Comment.objects.create(
            ticket=ticket,
            user=user,
            content=content,
            type=comment_type
        )

        TicketEvent.objects.create(
            ticket=ticket,
            event_type="COMMENT_ADDED",
            metadata={"type":comment_type}
        )
        if comment_type=="INTERNAL" and not user.is_staff:
            return Response(
                {"error":"Only admins can add internal comments"},
                status=403
            )

        return Response({"message":"comment added"})

class DashboardView(APIView):
    def get(self,request):
        now=timezone.now()

        #Total Tickets
        total_tickets=Ticket.objects.count()

        #open tickets
        open_tickets=Ticket.objects.filter(status="OPEN").count()

        #overdue tickets
        overdue_tickets=Ticket.objects.filter(
            sla_deadline__lt=now
        ).count()

        # Average resolution time - last 7 days
        last_7_days=now-timedelta(days=7)

        resolved_tickets=Ticket.objects.filter(
            status="RESOLVED",
            updated_at__gte=last_7_days
        ).annotate(
            resolution_time=ExpressionWrapper(
                F("updated_at")-F("created_at"),
                output_field=DurationField()
            )
        )

        avg_resolution_time=resolved_tickets.aggregate(
            avg_time=Avg("resolution_time")
        )["avg_time"]

        # category wise count
        category_data=Ticket.objects.values("category").annotate(
            count=Count("id")
        )

        return Response({
            "total_tickets":total_tickets,
            "open_tickets":open_tickets,
            "overdue_tickets":overdue_tickets,
            "avg_resolution_time":avg_resolution_time,
            "category_distribution":category_data,
        })
    
class UploadAttachmentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, pk):

        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)

        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file provided"}, status=400)

        attachment=Attachment.objects.create(

            ticket=ticket,
            file=file,
            file_size=file.size
        )

        # Event log
        TicketEvent.objects.create(
            ticket=ticket,
            event_type="ATTACHMENT_ADDED"
            )

        return Response({"message": "File uploaded"})

class OverridePriorityView(APIView):

    def post(self, request, pk):
        user = request.user

        if not user.is_staff:
            return Response({"error": "Admin only"}, status=403)

        try:
            ticket = Ticket.objects.get(pk=pk)
        except Ticket.DoesNotExist:
            return Response({"error": "Ticket not found"}, status=404)

        new_priority = request.data.get("priority")

        if new_priority not in ["P0", "P1", "P2", "P3"]:
            return Response({"error": "Invalid priority"}, status=400)

        old_priority = ticket.priority
        ticket.priority = new_priority
        ticket.save()

        # Event log
        TicketEvent.objects.create(
            ticket=ticket,
            event_type="PRIORITY_OVERRIDDEN",
            metadata={"from": old_priority, "to": new_priority}
        )

        return Response({"message": "Priority updated"})  

