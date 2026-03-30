from django.db import models
from django.contrib.auth.models import User

class StatusChoices(models.TextChoices):
    OPEN="OPEN","Open"
    IN_PROGRESS="IN_PROGRESS","In Progress"
    RESOLVED="RESOLVED","Resolved"
    CLOSED="CLOSED","Closed"

class PriorityChoices(models.TextChoices):
    PO="P0","Critical"
    P1="P1","High"
    P2="P2","Medium"
    P3="P3","LOW"

class CategoryChoices(models.TextChoices):
    BUG="BUG","Bug"
    FEATURE="FEATURE","Feature"
    BILLING="BILLING","Billing"
    OTHER="OTHER","Other"

class LevelChoices(models.TextChoices):
    LOW="LOW","Low"
    MEDIUM="MEDIUM","Medium"
    HIGH="HIGH","High"

class Ticket(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField()

    category=models.CharField(
        max_length=20,
        choices=CategoryChoices.choices
    )

    impact=models.CharField(
        max_length=10,
        choices=LevelChoices.choices
    )

    urgency=models.CharField(
        max_length=10,
        choices=LevelChoices.choices
    )

    priority=models.CharField(
        max_length=2,
        choices=PriorityChoices.choices
    )

    status=models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN
    )

    sla_deadline=models.DateTimeField()

    reopen_count=models.IntegerField(default=0)

    created_by=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    PUBLIC="PUBLIC"
    INTERNAL="INTERNAL"

    COMMENT_TYPE_CHOICES=[
        (PUBLIC,"Public"),
        (INTERNAL,"Internal"),
    ]

    ticket=models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()

    type=models.CharField(
        max_length=10,
        choices=COMMENT_TYPE_CHOICES,
        default=PUBLIC
    )

    created_at=models.DateTimeField(auto_now_add=True)

class Attachment(models.Model):
    ticket=models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="attachments"
    )
    file=models.FileField(upload_to="attachments/")
    file_size=models.IntegerField(null=True,blank=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)

class TicketEvent(models.Model):
    ticket=models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="events"
    )

    event_type=models.CharField(max_length=50)
    metadata=models.JSONField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)





