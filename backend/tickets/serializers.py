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
def validate_title(self, value):
    if len(value.strip()) < 5:
        raise serializers.ValidationError("Title must be at least 5 characters.")
    return value

def validate_description(self, value):
    if len(value.strip()) < 20:
        raise serializers.ValidationError("Description must be at least 20 characters.")
    return value