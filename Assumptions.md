# Assumptions

This system is designed as a generic **SaaS-based support desk platform**, where users raise tickets related to product issues such as bugs, billing problems, and feature requests.

## Domain Assumptions

* The system targets SaaS products (e.g., subscription-based platforms).
* Categories like **Billing**, **Bug**, and **Feature** are chosen to simulate realistic use cases.

## Priority Engine Assumptions

* Priority is **computed**, not selected by the user.
* Inputs considered:

  * Impact (Low / Medium / High)
  * Urgency (Low / Medium / High)
  * Category (Billing gets higher weight)
  * Reopen count
* Billing-related issues receive a **priority bump**.
* Reopened tickets increase priority level (escalation logic).

## SLA Assumptions

* SLA starts **at ticket creation time**.
* SLA is defined based on priority:

  * P0 → 4 hours
  * P1 → 12 hours
  * P2 → 24 hours
  * P3 → 72 hours
* SLA does **not pause** when status is "Resolved".
* SLA is **reset when a ticket is reopened**.
* Weekends are **included** in SLA calculation.

## User & Role Assumptions

* Two roles:

  * User → creates and views own tickets
  * Admin → views all tickets and manages system
* Authentication is implemented using Django’s built-in system.

## File Upload Assumptions

* Only one file can be uploaded per request.
* File size is limited (to prevent misuse).

## Event Tracking Assumptions

* Every important action is logged in `TicketEvent`.
* Events include:

  * Ticket creation
  * Status updates
  * Comments
  * File uploads
  * Reopen actions

## Simplifications

* No email notifications implemented.
* No real-time updates (polling-based UI).
* No advanced ML/NLP used for priority (rule-based only).
