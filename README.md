### ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/mohamadrezabjr/Ticket-System.git
cd Ticket-System

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure your database in settings.py or use a .env file

# 5. Apply migrations
python manage.py migrate

# 6. Create superuser (for admin access)
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver
```

