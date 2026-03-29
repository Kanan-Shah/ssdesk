ASSUMPTIONS

1.Priority Computation
  1.1 Priority is derived from the IMPACT and URGENCY
  1.2 Category can increase priority by one level(e.g., Billing Issues)
  1.3 Reopend tickets increase priority

2.SLA Rules
  2.1 SLA starts at ticket creation time
  2.2 SLA pauses when ticket is marked "Resolved"
  2.3 LA resets on ticket reopen 
  2.4 Weekends are ignored for simplicity

3.Status Transitions
  3.1 Valid: Open -> In Progress -> Resolved -> Closed
  3.2 Peopen allowed olny from Resolved/Closed

4.Users and Roles
  4.1 Users can only see their own tickets 
  4.2 Admins can view all tickets and add internal comments

5.Attachments
  5.1 Only one file allowed per ticket
  5.2 File Size Limit:25MB

6.Duplicate Detection
  Based on title Similarity

7.Background SLA checker
  Periodically checks overdue tickets

 