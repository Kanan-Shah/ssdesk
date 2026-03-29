from datetime import timedelta
from django.utils import timezone
SLA_RULES={
    "P0":4, #hours
    "P1":12,
    "P2":24,
    "P3":72
}

def compute_sla_deadline(priority,start_time=None):
    if not start_time:
        start_time=timezone.now()
    
    hours=SLA_RULES.get(priority,72)
    return start_time + timedelta(hours=hours)

def get_sla_remaining(sla_deadline):
    now=timezone.now()
    return sla_deadline - now

def is_sla_overdue(sla_dealine):
    return timezone.now() > sla_dealine

def get_overdue_duration(sla_deadline):
    if not is_sla_overdue(sla_deadline):
        return None
    
    return timezone.now() - sla_deadline

def recompute_sla_on_reopen(priority):
    return compute_sla_deadline(priority)

