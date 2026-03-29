# Database Schema

## Users

* id
* email
* role (USER / ADMIN)

---

## Tickets

* id
* title
* description
* category
* impact
* urgency
* priority
* status
* sla_deadline
* created_at
* updated_at
* reopen_count
* created_by (FK → Users.id)

---

## Comments

* id
* ticket_id (FK → Tickets.id)
* user_id (FK → Users.id)
* content
* type (PUBLIC / INTERNAL)
* created_at

---

## Attachments

* id
* ticket_id (FK → Tickets.id)
* file_path
* file_size
* uploaded_at

---

## TicketEvents

* id
* ticket_id (FK → Tickets.id)
* event_type
* metadata (JSON)
* created_at

---

# Relationships

* One User → Many Tickets
* One Ticket → Many Comments
* One Ticket → Many Events
* One Ticket → One or Many Attachments
* One User → Many Comments
