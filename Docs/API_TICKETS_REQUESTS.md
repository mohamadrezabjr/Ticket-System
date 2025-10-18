# 🧾 Ticket API - Example Requests & Responses

This document provides sample requests and responses for the Ticket endpoints (Tickets & Messages).

---

## 1️⃣ Tickets

### a) List Tickets

**Endpoint:** `/tickets/`  
**Method:** GET  
**Description:** List all tickets. Users see their own tickets; admin/support see all tickets.  

#### Sample Request
```http
GET /tickets/
Authorization: Bearer <access_token>
```

#### Sample Response

```json
HTTP 200 OK
[
  {
    "id": 1,
    "title": "Cannot login",
    "description": "I am unable to login with my mobile number",
    "category": "Login Issues",
    "user_status": "P",
    "admin_status": "N",
    "priority": "M",
    "client": 1,
    "created_at": "2025-10-18T09:00:00Z",
    "updated_at": "2025-10-18T09:05:00Z",
    "is_closed": false
  },
  {
    "id": 2,
    "title": "Payment failed",
    "description": "Payment did not go through",
    "category": "Billing",
    "user_status": "A",
    "admin_status": "A",
    "priority": "H",
    "client": 2,
    "created_at": "2025-10-17T12:30:00Z",
    "updated_at": "2025-10-17T13:00:00Z",
    "is_closed": false
  }
]
```

---

### b) Create Ticket

**Endpoint:** `/tickets/`  
**Method:** POST  
**Description:** Create a new ticket.  


#### Sample Request

```json
POST /tickets/
Authorization: Bearer <access_token>
{
  "title": "New Issue",
  "description": "Description of the issue here",
  "category": 1,
  "priority": "H"
}
```

#### Sample Response

```json
HTTP 201 Created
{
  "id": 3,
  "title": "New Issue",
  "description": "Description of the issue here",
  "category": "Login Issues",
  "user_status": "P",
  "admin_status": "N",
  "priority": "H",
  "client": 1,
  "created_at": "2025-10-18T11:00:00Z",
  "updated_at": "2025-10-18T11:00:00Z",
  "is_closed": false
}
```

---

### c) Get Ticket Details

**Endpoint:** `/tickets/<ticket_id>/`  
**Method:** GET  
**Description:** Get detailed info about a ticket.  

#### Sample Request

```http
GET /tickets/3/
Authorization: Bearer <access_token>
```

#### Sample Response

```json
HTTP 200 OK
{
  "id": 3,
  "title": "New Issue",
  "description": "Description of the issue here",
  "category": "Login Issues",
  "user_status": "P",
  "admin_status": "N",
  "priority": "H",
  "client": 1,
  "created_at": "2025-10-18T11:00:00Z",
  "updated_at": "2025-10-18T11:00:00Z",
  "is_closed": false,
}
```

---

## 2️⃣ Messages

### a) List Messages

**Endpoint:** `/tickets/<ticket_id>/messages/`  
**Method:** GET  
**Description:** List all messages of a ticket.  

#### Sample Request

```http
GET /tickets/3/messages/
Authorization: Bearer <access_token>
```

#### Sample Response

```json
HTTP 200 OK
[
  {
    "id": 1,
    "ticket": 3,
    "sender": 1,
    "body": "I have an issue with login",
    "file": null,
    "created_at": "2025-10-18T11:05:00Z"
  },
  {
    "id": 2,
    "ticket": 3,
    "sender": 2,
    "body": "Please provide more details",
    "file": null,
    "created_at": "2025-10-18T11:10:00Z"
  }
]
```

---

### b) Send a Message

**Endpoint:** `/tickets/<ticket_id>/messages/`  
**Method:** POST  
**Description:** Send a message in a ticket (supports file attachment).  

#### Sample Request

```json
POST /tickets/3/messages/
Authorization: Bearer <access_token>
{
  "body": "Here is the screenshot",
  "file": "screenshot.png"
}
```

#### Sample Response

```json
HTTP 201 Created
{
  "id": 3,
  "ticket": 3,
  "sender": 1,
  "body": "Here is the screenshot",
  "file": "files/ticket_3/message_3_screenshot.png",
  "created_at": "2025-10-18T11:20:00Z"
}
```

---

### c) Update ticket

**Endpoint:** `/tickets/<ticket_id>/`  
**Method:** PATCH  
**Description:** Updates a ticket.  

#### Sample Request

```json
PATCH /tickets/3/
Authorization: Bearer <access_token>
{
  "title": "New Issue"
}
```

#### Sample Response

```json
HTTP 200 OK
{
  "id": 3,
  "title": "New Issue",
  "description": "Description of the issue here",
  "category": "Login Issues",
  "user_status": "P",
  "admin_status": "S",
  "priority_display": "فوری-بالا",
  "admin_status_display": "دیده شده",
  "user_status_display": "در انتظار پاسخ",
  "priority": "H",
  "client": 1,
  "created_at": "2025-10-18T11:00:00Z",
  "updated_at": "2025-10-18T11:25:00Z",
  "is_closed": false,
  
}
```
---

### d) Cloes ticket

**Endpoint:** `/tickets/<ticket_id>/close/`  
**Method:** GET or POST  
**Description:** close a ticket.  

#### Sample Request

```json
PATCH /tickets/3/
Authorization: Bearer <access_token>
```

#### Sample Response

```json
HTTP 200 OK
{
    "message": "Ticket #3 successfully closed."
}
```
---
## 3️⃣ Ticket Categories

### a) List Categories

**Endpoint:** `/ticket-categories/`    
**Method:** GET  
**Description:** List all ticket categories.  

### Sample Request
```http
GET /ticket-categories/
Authorization: Bearer <access_token>
```

### Sample Response

```json
HTTP 200 OK
[
  {
    "id": 1,
    "name": "Login Issues",
    "description": "Problems related to logging in"
  },
  {
    "id": 2,
    "name": "Billing",
    "description": "Payment and billing related issues"
  }
]
```

---

### b) Create Category

**Endpoint:** `/ticket-categories/`  
**Method:** POST  
**Description:** Create a new ticket category. Admin only.

### Sample Request

```json
POST /ticket-categories/
Authorization: Bearer <admin_access_token>
{
  "name": "Technical Support",
  "description": "Technical issues and system bugs"
}
```

### Sample Response

```json
HTTP 201 Created
{
  "id": 3,
  "name": "Technical Support",
  "description": "Technical issues and system bugs"
}
```

---

### c) Get Category Details

**Endpoint:** `/ticket-categories/<category_id>/`  
**Method:** GET  
**Description:** Retrieve details of a specific ticket category.  

### Sample Request

```http
GET /ticket-categories/3/
Authorization: Bearer <access_token>
```

### Sample Response

```json
HTTP 200 OK
{
  "id": 3,
  "name": "Technical Support",
  "description": "Technical issues and system bugs"
}
```

---

### d) Update Category

**Endpoint:** `/ticket-categories/<category_id>/`  
**Method:** PATCH  
**Description:** Update a ticket category. Admin only.  

### Sample Request

```json
PATCH /ticket-categories/3/
Authorization: Bearer <admin_access_token>
{
  "description": "Updated description for technical support"
}
```

### Sample Response

```json
HTTP 200 OK
{
  "id": 3,
  "name": "Technical Support",
  "description": "Updated description for technical support"
}
```


---
