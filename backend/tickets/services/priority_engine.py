PRIORITY_ORDER=["P0","P1","P2","P3"] # lower index = high priority

def get_base_priority(impact,urgency):
    if impact=="HIGH" and urgency=="HIGH":
        return "P0"
    
    if impact=="HIGH" or urgency=="HIGH":
        return "P1"
    
    if impact=="MEDIUM" or urgency=="MEDIUM":
        return "P2"
    
    return "P3"

# in any case priority needs to be increased , such as category wise
def escalate_priority(priority,levels=1):
    index=PRIORITY_ORDER.index(priority)
    new_index=max(0,index-levels)
    return PRIORITY_ORDER[new_index]
# P2->P1 , P1->P0 , P0->P0

CRITICAL_KEYWORDS=[
    "payment failed",
    "money debited",
    "transaction error",
    "refund not received",
    "system down",
]

def has_critical_keywords(text):
    text=text.lower()
    return any(keyword in text for keyword in CRITICAL_KEYWORDS)

def compute_priority(impact,urgency,category,description,reopen_count):
    #step 1 Base Priority
    priority=get_base_priority(impact,urgency)

    #step 2 Category boost
    if category=="BILLING":
        priority=escalate_priority(priority)
    
    #step 3 Keyword Override
    if has_critical_keywords(description):
        priority="P0"

    #step 4 Reopen escalation
    if reopen_count>=2:
        priority=escalate_priority(priority)

    return priority
 

# FLOW: BASE -> CATEGORY -> KEYWORDS -> REOPEN -> FINAL PRIORITY
