# Database Schema

The system follows a normalized relational design.

## Entities

### User

* id (Primary Key)
* username
* password

---

### Ticket

* id (Primary Key)
* title
* description
* category (Bug / Feature / Billing / Other)
* impact (Low / Medium / High)
* urgency (Low / Medium / High)
* priority (P0 / P1 / P2 / P3)
* status (Open / In Progress / Resolved / Closed)
* created_by (ForeignKey → User)
* sla_deadline (DateTime)
* reopen_count (Integer)
* created_at (DateTime)
* updated_at (DateTime)

---

### Comment

* id (Primary Key)
* ticket (ForeignKey → Ticket)
* user (ForeignKey → User)
* content
* type (Public / Internal)
* created_at (DateTime)

---

### Attachment

* id (Primary Key)
* ticket (ForeignKey → Ticket)
* file
* file_size
* uploaded_at (DateTime)

---

### TicketEvent

* id (Primary Key)
* ticket (ForeignKey → Ticket)
* event_type (TICKET_CREATED, STATUS_CHANGED, etc.)
* created_at (DateTime)

---

## Relationships

* One User → Many Tickets
* One Ticket → Many Comments
* One Ticket → Many Attachments
* One Ticket → Many Events

---

## Queryability

Ticket history is fully queryable via:

GET /api/tickets/{id}/events/

This enables:

* Audit tracking
* Timeline reconstruction
* Analytics computation
