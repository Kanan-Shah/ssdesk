from rest_framework import serializers
from .models import Ticket
# validates input , converts JSON <-> Model
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields=[
            "id",
            "title",
            "description",
            "category",
            "impact",
            "urgency",
            "priority",
            "status",
            "sla_deadline",
            "created_at",
            "updated_at"

        ]
        read_only_fields=[
            "id",
            "priority",
            "sla_deadline",
            "status",
            "created_at",
            "updated_at",
            "reopen_count"
            ]
