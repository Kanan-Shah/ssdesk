# Smart Support Desk System

## Overview

This is an end-to-end web application that allows users to raise support tickets while the system intelligently determines **priority**, **SLA timelines**, and provides **analytics**.

The system is designed to simulate a real-world SaaS support desk with structured workflows, rule-based computation, and event tracking.

---
## Project Structure
```
ssdesk/
├── config/              # Django project config
│   ├── settings.py
│   ├── urls.py
├── tickets/             # Main app
│   ├── models.py        # Ticket, Comment, Attachment, TicketEvent
│   ├── views.py         # All API + page views
│   ├── serializers.py
│   ├── api_urls.py      # /api/tickets/ routes
│   ├── page_urls.py     # /tickets/ page routes
│   ├── services/
│   │   ├── priority_engine.py
│   │   └── sla_engine.py
│   ├── tests.py
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── signup.html
│       ├── ticket_list.html
│       ├── ticket_create.html
│       ├── ticket_detail.html
│       └── dashboard.html
├── manage.py
├── README.md
├── ASSUMPTIONS.md
├── API.md
└── DB_SCHEMA.md
```
---

## Features

### Authentication

* User signup & login
* Role-based access (User / Admin)

### Ticket Management

* Create tickets with:

  * Title, Description
  * Category, Impact, Urgency
  * Optional file attachment
* Automatic priority computation (P0–P3)
* SLA deadline assignment

### Ticket Workflow

* Status transitions:

  * Open → In Progress → Resolved → Closed
* Reopen tickets with escalation

### Comments

* Public comments (user & admin)
* Internal comments (admin only)

### Attachments

* File upload support
* Metadata stored in database

### Dashboard

* Total tickets
* Open tickets
* Overdue tickets
* Average resolution time
* Category distribution
* User-wise ticket distribution

### Event Tracking

* Every action generates a `TicketEvent`
* Supports analytics and auditability

---

## Tech Stack

* Backend: Django + Django REST Framework
* Frontend: Django Templates + JavaScript
* Database: SQLite (can be replaced with PostgreSQL)

---

## API Endpoints

| Endpoint                        | Description    |
| ------------------------------- | -------------- |
| POST /api/tickets/create/       | Create ticket  |
| GET /api/tickets/               | List tickets   |
| GET /api/tickets/{id}/          | Ticket detail  |
| POST /api/tickets/{id}/status/  | Update status  |
| POST /api/tickets/{id}/comment/ | Add comment    |
| POST /api/tickets/{id}/upload/  | Upload file    |
| GET /api/tickets/dashboard/     | Dashboard data |
| GET /api/tickets/{id}/events/   | Ticket history |

---

## Setup Instructions

### 1. Clone repository

```bash
git clone <repo-url>
cd ssdesk/backend
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install django djangorestframework pillow
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Create superuser (admin)

```bash
python manage.py createsuperuser
```

### 6. Run server

```bash
python manage.py runserver
```

---

## Access

* User UI → http://127.0.0.1:8000/
* Admin panel → http://127.0.0.1:8000/admin/

---

## Key Design Decisions

* Priority is rule-based (Impact + Urgency + Category + Reopen count)
* SLA is computed dynamically and tracked per ticket
* Event history enables full audit trail
* Separation of API and UI layers
* Role-based access ensures security

---

## Future Improvements

* Real-time updates (WebSockets)
* ML-based priority classification
* Email notifications
* Advanced analytics dashboard

---

## Conclusion

This system demonstrates:

* Backend design
* Business logic modeling
* API design
* Data modeling
* Full-stack integration

It is built with clarity, scalability, and real-world use cases in mind.
