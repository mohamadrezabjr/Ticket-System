# 🧾 TicketSystem API Endpoints

This document lists all API endpoints for the TicketSystem project, including authentication, tickets, admin, and notifications. It also references API schema and documentation URLs.

---

## 🌐 Base URLs

| Path      | Description |
|-----------|-------------|
| `/django-admin/` | Django admin panel |
| `/`       | Ticket app endpoints |
| `/auth/`  | Authentication endpoints (register, login, logout, profile) |
| `/admin/` | Admin panel API endpoints (users & notifications) |
| `/api/schema/` | OpenAPI JSON schema |
| `/swagger/` | Swagger UI |
| `/redoc/` | Redoc UI |

---

## 1️⃣ Auth Endpoints

| Endpoint | Method | Description | Permissions |
|----------|--------|-------------|-------------|
| `/auth/login/` | POST | Obtain JWT access & refresh token | Public |
| `/auth/token/refresh/` | POST | Refresh JWT access token | Public |
| `/auth/register/` | POST | User registration | Public |
| `/auth/logout/` | POST | Logout user, invalidate token | Authenticated |

### Profile
| Endpoint | Method | Description | Permissions |
|----------|--------|-------------|-------------|
| `/auth/profile/<user_id>/` | GET | Get user profile details | Authenticated |
| `/auth/profile/update/<user_id>/` | PATCH | Update user profile | Authenticated |

> For full example requests and responses, see [Auth API – Authentication & Profile](Docs/API_AUTH_REQUESTS.md).

---

## 2️⃣ Admin Panel Endpoints

### Users
| Endpoint | Method | Description | Permissions |
|----------|--------|-------------|-------------|
| `/admin/users/` | GET | List all users | Admin |
| `/admin/users/` | POST | Create a new user | Admin |
| `/admin/users/<user_id>/` | GET | Get user details | Admin |
| `/admin/users/<user_id>/` | PATCH | Update user info | Admin |


### Notifications
| Endpoint                                  | Method | Description | Permissions |
|-------------------------------------------|--------|-------------|-------------|
| `/admin/notifications/`                   | GET | List all notifications for the user | Authenticated |
| `/admin/notifications/`                   | POST | Create a new notification | Admin |
| `/admin/notifications/<notification_id>/` | GET | Get notification details | Authenticated |
| `/admin/notifications/<notification_id>/` | PATCH | Update a notification | Admin |
| `/admin/notifications/<notification_id>/` | DELETE | Delete a notification | Admin |
> For full example requests and responses, see [Admin API – Users & Notifications](Docs/API_ADMIN_REQUESTS.md).

---

## 3️⃣ Ticket Endpoints

| Endpoint                            | Method      | Description                                     | Permissions   |
|-------------------------------------|-------------|-------------------------------------------------|---------------|
| `/tickets/`                         | GET         | List all tickets (user: own tickets)            | Authenticated |
| `/tickets/`                         | POST        | Create a new ticket                             | Authenticated |
| `/tickets/<ticket_id>/`             | GET         | Get ticket details                              | Authenticated |
| `/tickets/<ticket_id>/close/`       | GET or POST | Close a ticket                                  | Authenticated |
| `/tickets/<ticket_id>/messages/`    | GET         | List messages of a ticket                       | Authenticated |
| `/tickets/<ticket_id>/messages/`    | POST        | Send a message in the ticket (supports file attachments) | Authenticated |
| `/ticket-categories/`               | GET         | List all tickets (user: own tickets)            | Authenticated |
| `/ticket-categories/`               | POST        | Create a new ticket category                    | Admin         |
| `/ticket-categories/<category_id>/` | GET         | Get ticket category details                     | Authenticated |
| `/ticket-categories/<ticket_id>/`   | PATCH       | moddify a ticket cateogry                       | Authenticated |

> For full example requests and responses, see the [Ticket API – Tickets & Messages](Docs/API_TICKETS_REQUESTS.md) document.

---

## Notes
- All endpoints require JWT authentication unless marked as Public.  
- Roles and permissions are enforced at the backend (User, Support, Admin).  
- Swagger UI (`/swagger/`) and Redoc (`/redoc/`) can be used for interactive API testing.
