ASSUMPTIONS

1.Priority Computation
  - Priority is derived from the IMPACT and URGENCY
  - Category can increase priority by one level(e.g., Billing Issues)
  - Reopend tickets increase priority

2.SLA Rules
  - SLA starts at ticket creation time
  - SLA pauses when ticket is marked "Resolved"
  - LA resets on ticket reopen 
  - Weekends are ignored for simplicity

3.Status Transitions
  - Valid: Open -> In Progress -> Resolved -> Closed
  - Peopen allowed olny from Resolved/Closed

4.Users and Roles
  - Users can only see their own tickets 
  - Admins can view all tickets and add internal comments

5.Attachments
  - Only one file allowed per ticket
  - File Size Limit:25MB

6.Duplicate Detection
 - Based on title Similarity

7.Background SLA checker
 - Periodically checks overdue tickets

 
