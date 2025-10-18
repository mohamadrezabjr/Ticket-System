---

# 🧾 Admin API - Example Requests & Responses

This document provides sample requests and responses for the Admin API endpoints (Users & Notifications).

---

## 1️⃣ Users

### a) List Users

**Endpoint:** `/admin/users/`  
**Method:** GET  
**Description:** List all users. Admin only.  

#### Sample Request
```http
GET /admin/users/
Authorization: Bearer <admin_access_token>
```

#### Sample Response

```json
HTTP 200 OK
[
  {
    "id": 1,
    "mobile": "+989123456789",
    "city": "Tehran",
    "province": "Tehran",
    "role": "user"
  },
  {
    "id": 2,
    "mobile": "+989987654321",
    "city": "Shiraz",
    "province": "Fars",
    "role": "support"
  }
]
```

---

### b) Create User

**Endpoint:** `/admin/users/`
**Method:** POST
**Description:** Create a new user. Admin only.

#### Sample Request

```json
POST /admin/users/
Authorization: Bearer <admin_access_token>
{
  "phone": "+989111222333",
  "password": "NewUserPassword123",
  "username" : "username"      
  "email" : "Email",
  "role": "user",
  "image" : "image"
}
```

#### Sample Response

```json
HTTP 201 Created
{
  "id": 3,
  "phone": "+989111222333",
  "password": "NewUserPassword123",
  "username" : "username"      
  "email" : "Email",
  "role": "user",
  "image" : "image"
}
```

---

### c) Get User Details

**Endpoint:** `/admin/users/<user_id>/`
**Method:** GET
**Description:** Get details of a specific user. Admin only.

#### Sample Request

```http
GET /admin/users/3/
Authorization: Bearer <admin_access_token>
```

#### Sample Response

```json
HTTP 200 OK
{
  "id": 3,
  "phone": "+989111222333",
  "city": "Mashhad",
  "province": "Khorasan",
  "role": "user",
  "email": "user@example.com",
  "username": "string",
  "image": "string"
}
```

---

### d) Update User

**Endpoint:** `/admin/users/<user_id>/`
**Method:** PATCH
**Description:** Update user information. Admin only.

#### Sample Request

```json
PATCH /admin/users/3/
Authorization: Bearer <admin_access_token>
{
  ""
  "role": "support"
}
```

#### Sample Response

```json
HTTP 200 OK
{
  "id": 3,
  "phone": "+989111222333",
  "city": "Mashhad",
  "province": "Khorasan",
  "role": "user",
  "email": "user@example.com",
  "username": "string",
  "image": "string"
}
```

---

## 2️⃣ Notifications

### a) List Notifications

**Endpoint:** `/admin/notifications/`
**Method:** GET
**Description:** List all notifications for the authenticated user.

#### Sample Request

```http
GET /admin/notifications/
Authorization: Bearer <access_token>
```

#### Sample Response

```json
HTTP 200 OK
[
  {
    "id": 1,
    "category": "Info",
    "description" : "Test",
    "seen": false,
    "created_at": "2025-10-18T08:00:00Z"
  },
  {
    "id": 2,
    "category": "warning",
    "description": "A new ticket category 'Billing' has been created.",
    "seen": true,
    "created_at": "2025-10-17T15:30:00Z"
  }
]
```

---

### b) Create Notification

**Endpoint:** `/admin/notifications/`
**Method:** POST
**Description:** Create a new notification. Admin only.

#### Sample Request

```json
POST /admin/notifications/
Authorization: Bearer <admin_access_token>
{
  "category": "info",
  "message": "Server will be updated at 2 AM tomorrow.",
  "user_ids": [1, 2, 3]
}
```

#### Sample Response

```json
HTTP 201 Created
{
  "id": 3,
  "category": "warning",
  "message": "Server will be updated at 2 AM tomorrow.",
  "created_at": "2025-10-18T10:00:00Z"
}
```

---

### c) Get Notification Details

**Endpoint:** `/admin/notifications/<notification_id>/`
**Method:** GET
**Description:** Get details of a specific notification. Authenticated user only.

#### Sample Request

```http
GET /admin/notifications/3/
Authorization: Bearer <access_token>
```

#### Sample Response

```json
HTTP 200 OK
{
  "id": 3,
  "category": "warning",
  "message": "Server will be updated at 2 AM tomorrow.",
  "seen": false,
  "created_at": "2025-10-18T10:00:00Z"
}
```

---

### d) Update Notification

**Endpoint:** `/admin/notifications/<notification_id>/`
**Method:** PATCH
**Description:** Update notification content. Admin only.

#### Sample Request

```json
PATCH /admin/notifications/3/
Authorization: Bearer <admin_access_token>
{
  "title": "Server maintenance",
  "content": "Server maintenance rescheduled to 3 AM."
}
```

#### Sample Response

```json
HTTP 200 OK
{
  "id": 3,
  "category": "Info",
  "message": "Server maintenance rescheduled to 3 AM.",
  "seen": false,
  "created_at": "2025-10-18T10:00:00Z"
}
```

---

### e) Delete Notification

**Endpoint:** `/admin/notifications/<notification_id>/`
**Method:** DELETE
**Description:** Delete a notification. Admin only.

#### Sample Request

```http
DELETE /admin/notifications/3/
Authorization: Bearer <admin_access_token>
```

#### Sample Response

```json
HTTP 204 No Content
{}
```
