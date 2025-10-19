# 🎫 TicketSystem

**TicketSystem** is a support ticket management platform designed to handle user issues and support requests efficiently.  
It allows users to submit tickets, communicate with support staff, and receive updates in real time.

---

## 🚀 Features

### 👤 User Features
- Register and log in using **mobile number**  
- Create new **support tickets** with optional file attachments  
- View ticket details, status, and conversation history  
- Send and receive **real-time messages** within a ticket (via WebSocket)  
- Close tickets manually when the issue is resolved  
- Receive **notifications** inside the app, via **email**, and **SMS**  
- Manage personal profile (city, province, and profile picture)

---

### 🧰 Support Features
- View all assigned or open tickets  
- Reply to user messages in real time  
- Close tickets after resolution  
- Access to categorized ticket lists for better organization  

---

### 🛡️ Admin Features
- Full access to all tickets, users, and system data  
- Manage **categories** (create, edit, delete)  
- Manage **users** and their roles (Admin, Support, User)  
- Send **notifications** to users or specific roles (via in-app, email, and SMS)  
- Monitor overall ticket activity and system health  

---

### ⚡ System Features
- Authentication via **JWT** and **Session**  
- Real-time communication powered by **Django Channels**  
- Role-based permission control  
- Modular and scalable architecture (DRF-based API only)  
- Containerized environment using **Docker Compose**  


---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Django, Django REST Framework |
| Authentication | JWT, Session |
| Real-time Communication | Django Channels |
| Database | PostgreSQL |
| Caching / Queue (optional) | Redis |
| Containerization | Docker & Docker Compose |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/mohamadrezabjr/Ticket-System.git
cd Ticket-System
```

### 2. Create your environment file
Copy the example file and fill in your own values:
```bash
cp .env.example .env
```

Edit `.env` and set your values:
```
ENVIRONMENT=development
SECRET_KEY=your-secret-here
REDIS_HOST=redis
REDIS_PORT=6379
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

> ⚠️ Do **not** commit your `.env` file to the repository. Keep it private.

### 3. Run with Docker Compose
```bash
docker-compose up --build
```

### 4. Run migrations
```bash
docker-compose exec web python manage.py migrate
```

### 5. Create a superuser
```bash
docker-compose exec web python manage.py createsuperuser
```

Then visit:  
👉 http://localhost:8000/django-admin


---

## 📚 API Overview

| Area | Endpoint Examples |
|------|--------------------|
| Auth | `/signup`, `/login`, `/logout`, `/profile` |
| Tickets | `/tickets`, `/tickets/{id}`, `/tickets/{ticket_id}/messages` |
| Categories | `/categories`, `/categories/{category_id}` |
| Admin | `/notifications`, `/users` |

Full API documentation is available in the upcoming **API_DOCUMENTATION.md** file.

---

## 📂 Project Structure
```
Ticket-System/
│
├── admin_app/                 # Admin pannel
├── auth_app/                 # User & profile management
├── ticket_system/         # Main Django project folder
├── ticket_app/               # Ticket app (ticket & messages)
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

---

## 👥 Roles & Permissions

| Role | Description |
|------|--------------|
| **Admin** | Full access to manage users, categories, and notifications |
| **Support** | Can view and respond to tickets |
| **User** | Can create and view own tickets |

---

## 🧪 Development Notes

- Real-time communication handled via **Django Channels** and WebSockets  
- JWT authentication for API requests  
- Separate admin endpoints for management tasks  
- Modular app structure for scalability  

