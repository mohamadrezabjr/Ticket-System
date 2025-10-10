# 🧭 How to Work on This Project

### 1️⃣ Clone the project (first time only)
```bash
git clone https://github.com/mohamadrezabjr/Ticket-System.git
cd Ticket-System
```

---

### 2️⃣ Switch to the `dev` branch
```bash
git checkout dev
```
If you don’t have it:
```bash
git fetch origin
git checkout dev
```

---

### 3️⃣ Pull the latest changes before you start
```bash
git pull origin dev
```

---

### 4️⃣ Make your changes and commit
```bash
git add .
git commit -m "your short commit message"
```

Example:
```bash
git commit -m "fix: user registration issue"
```

---

### 5️⃣ Push your changes to `dev`
```bash
git push origin dev
```

If you get an error (someone pushed before you):
```bash
git pull origin dev
# resolve conflicts if any
git push origin dev
```

---

### ⚠️ Important
- **Never push to `main`** — it’s protected.  
- Only the project lead can merge `dev` into `main`.
