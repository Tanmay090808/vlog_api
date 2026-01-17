# Vlog API — FastAPI Backend with JWT Authentication & Email Verification

A production-style backend API built using **FastAPI** that implements secure authentication, email verification, and a modular architecture suitable for real-world applications and internships.

This project goes beyond basic CRUD by handling real system-level concerns like token security, environment-based configuration, SMTP integration, and route-prefix debugging.

---

## 🚀 Features

* **User Registration & Login**
* **JWT Authentication**

  * Access Tokens
  * Refresh Tokens
* **Email Verification System**

  * Expiring verification tokens
  * URL-safe verification links
  * Login blocked for unverified users
* **Secure Password Hashing** (bcrypt)
* **Environment-Based Configuration**

  * Secrets & credentials stored in `.env`
* **Modular Project Structure**

  * Clean separation of routes, services, models, schemas, and utilities

---

## 🧱 Tech Stack

* **Backend:** FastAPI (Python)
* **Database:** PostgreSQL / SQLite (SQLAlchemy ORM)
* **Authentication:** JWT (python-jose)
* **Email Service:** SMTP (Gmail / Mailtrap supported)
* **Security:** Passlib (bcrypt)
* **Environment Config:** python-dotenv

---

## 📂 Project Structure

````text
vlog_api/
├── src/
│   ├── __pycache__/
│   ├── db/                 # Database setup, session, and models
│   ├── routes/            # API route handlers
│   │   ├── auth.py            # Auth & email verification endpoints
│   │   ├── blog_upload.py    # Blog creation & upload endpoints
│   │   └── blog_commenting.py # Blog comments endpoints
│   ├── util/             # Shared utilities
│   │   ├── dependencies.py   # FastAPI dependencies (DB, auth, etc.)
│   │   ├── email_verification.py # SMTP & email sending logic
│   │   ├── jwt_utils.py     # JWT creation & validation
│   │   ├── oauth2.py        # OAuth2 / token helpers
│   │   └── password_hashing.py # Password hashing utilities
│   └── main.py          # FastAPI app entry point
├── venv/               # Python virtual environment
├── .env               # Environment variables (ignored by Git)
├── .gitignore
└── README.md
```text
vlog_api/
├── src/
│   ├── core/        # Config & environment loading
│   ├── /     # Database models
│   ├── routes/     # API routes (auth, users, etc.)
│   ├── schemas/   # Pydantic schemas
│   ├── util/      # JWT & email utilities
│   └── main.py    # FastAPI app entry point
├── .env.example
├── requirements.txt
└── README.md
````

---

## 🔐 Authentication Flow

```text
Register
  ↓
User saved in DB (is_verified = false)
  ↓
Verification JWT generated
  ↓
Email sent with verification link
  ↓
User clicks link
  ↓
Token verified → is_verified = true
  ↓
Login allowed → Access & Refresh tokens issued
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/Tanmay090808/vlog_api.git
cd vlog_api
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Environment Variables

Create a `.env` file using the template below:

```env
SECRET_KEY=supersecretkey123
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
```

⚠️ Use **Gmail App Passwords** or **Mailtrap** for testing.

---

## ▶️ Run Server

```bash
uvicorn src.main:app --reload
```

Open Swagger UI:

```text
http://localhost:8000/docs
```

---

## 🔎 API Endpoints

### Authentication

| Method | Endpoint                    | Description               |
| ------ | --------------------------- | ------------------------- |
| POST   | `/user/register`            | Register new user         |
| POST   | `/user/login`               | Login user                |
| GET    | `/user/verify-email`        | Verify email via token    |
| POST   | `/user/resend-verification` | Resend verification email |

---

## 🧪 Testing Email Verification

1. Register a new user
2. Check email inbox for verification link
3. Click link in browser
4. Confirm response:

```json
{
  "message": "Email verified successfully"
}
```

---

## 🧠 Key Learnings

* JWT payload validation and expiration handling
* Secure secret management using environment variables
* SMTP integration and debugging authentication failures
* Router prefix debugging in FastAPI
* URL-safe token handling in verification links

---

## 📌 Future Improvements

* Role-based access control (RBAC)
* Rate limiting
* Password reset flow
* WebSocket-based real-time features
* Docker deployment

---

## 👨‍💻 Author

**Tanmay Babasaheb Ghadge**
Diploma in Computer Engineering | Backend Developer

GitHub: [https://github.com/Tanmay090808](https://github.com/Tanmay090808)

---

## 📜 License

This project is licensed under the **MIT License**. Feel free to use and modify it for learning and development.
