
# 🧾 Auth API - Example Requests & Responses

This document provides sample requests and responses for the authentication and profile endpoints.

---

## 1️⃣ Register

**Endpoint:** `/auth/register/`  
**Method:** POST  
**Description:** Register a new user using mobile number.  

### Sample Request
```json
POST /auth/register/
{
  "mobile" : "09123456789",
  "password":  "StrongPassword123"
}
```
### Sample Response

```json
HTTP 201 Created
{
    "user": {
        "phone": "09123456789"
    },
    "token": {
        "access-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiw ...",
        "refresh-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaC ..."
    }
}
```

---

## 2️⃣ Login

**Endpoint:** `/auth/login/`
**Method:** POST
**Description:** Obtain JWT access and refresh tokens.

### Sample Request

```json
POST /auth/login/
{
  "mobile": "+989123456789",
  "password": "StrongPassword123"
}
```

### Sample Response

```json
HTTP 200 OK
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 3️⃣ Token Refresh

**Endpoint:** `/auth/token/refresh/`
**Method:** POST
**Description:** Refresh JWT access token using refresh token.

### Sample Request

```json
POST /auth/token/refresh/
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Sample Response

```json
HTTP 200 OK
{
  "access": "newAccessTokenHere"
}
```

---

## 4️⃣ Logout

**Endpoint:** `/auth/logout/`
**Method:** POST
**Description:** Logout user and invalidate the refresh token.

### Sample Request

```json
POST /auth/logout/
Authorization: Bearer <access_token>
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Sample Response

```json
HTTP 204 No Content
{}
```

---

## 5️⃣ Get Profile

**Endpoint:** `/auth/profile/<user_id>/`
**Method:** GET
**Description:** Get profile details for a specific user.

### Sample Request

```http
GET /auth/profile/1/
Authorization: Bearer <access_token>
```

### Sample Response

```json
HTTP 200 OK
{
  "id": 1,
{
    "user": "09*******",
    "username": "example",
    "email": "example@example.com",
    "city": "Tehran",
    "province": "Tehran",
    "image": "/media/profiles/..."
}

```

---

## 6️⃣ Update Profile

**Endpoint:** `/auth/profile/update/<user_id>/`
**Method:** PATCH
**Description:** Update user profile information.

### Sample Request

```json
PATCH /auth/profile/update/1/
Authorization: Bearer <access_token>
{
  "city": "Shiraz",
  "province": "Fars"
  "username" : "example",
}
```

### Sample Response

```json
HTTP 200 OK
{
  "phone": "+989123456789",
  "email" : "example@example.com",        
  "username" : "example",
  "city": "Shiraz",
  "province": "Fars",
  "image": null,
}
```

