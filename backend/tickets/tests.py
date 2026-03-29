from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from tickets.services.priority_engine import compute_priority
from tickets.services.sla_engine import compute_sla_deadline,is_sla_overdue

class CoreLogicTests(TestCase):
    def test_priority_computation(self):
        priority=compute_priority(
            impact="MEDIUM",
            urgency="MEDIUM",
            category="BILLING",
            description="money debited",
            reopen_count=0
        )
        self.assertEqual(priority,"P0")

    def test_sla_deadline(self):
        deadline=compute_sla_deadline("P1")
        diff=deadline -timezone.now()
        self.assertTrue(diff<=timedelta(hours=12))
    
    def test_sla_overdue(self):
        past_time=timezone.now() - timedelta(hours=5)
        self.assertTrue(is_sla_overdue(past_time))
    
    def test_status_transition_invalid(self):
        from tickets.views import VALID_TRANSITIONS
        self.assertNotIn("CLOSED",VALID_TRANSITIONS["OPEN"])
    
    def test_reopen_escalation(self):
        priority=compute_priority(
            impact="LOW",
            urgency="LOW",
            category="BUG",
            description="minor issue",
            reopen_count=2
        )
        self.assertEqual(priority,"P2")