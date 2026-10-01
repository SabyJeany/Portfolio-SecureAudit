# 🔒 SecureAudit — Automated Web Security Audit Platform

> Analyze your website security in less than 10 seconds. No technical skills needed.

![SecureAudit](https://img.shields.io/badge/SecureAudit-v1.0-1D9E75?style=flat-square)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138-009688?style=flat-square)
![React](https://img.shields.io/badge/React-19-61DAFB?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=flat-square)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Security Checks](#security-checks)
- [Team](#team)

---

## 🎯 Overview

SecureAudit is a SaaS web application that allows any user — technical or not — to audit the security of a website by simply entering a URL.

**The problem it solves:**
Small businesses and independent developers own websites without the resources or expertise to assess their security posture. Cyberattacks cost an average of $4.45M per incident, yet most vulnerabilities are detectable and fixable.

**The solution:**
SecureAudit automates the audit process and presents results as a clear, color-coded report with a 0-100 security score, prioritized findings, and plain-language explanations for each vulnerability detected.

---

## ✨ Features

- 🔍 **URL Scanner** — analyze any website in under 10 seconds
- 📊 **Security Score** — 0-100 score with visual gauge and severity label
- 🛡️ **9 Security Checks** — headers, SSL, redirects, robots.txt and more
- 📚 **Educational Cards** — plain-language explanations for each finding
- 📄 **PDF Export** — professional downloadable security report
- 🕐 **Scan History** — track your security improvements over time
- 🔐 **User Accounts** — JWT authentication with bcrypt password hashing

---

## 🚀 Tech Stack

### Frontend
| Technology | Purpose |
|---|---|
| React.js + Vite | UI framework |
| Tailwind CSS | Styling |
| React Router DOM | Navigation |
| Axios | API calls |

### Backend
| Technology | Purpose |
|---|---|
| Python FastAPI | REST API |
| SQLAlchemy | ORM |
| PostgreSQL | Database |
| JWT + bcrypt | Authentication |
| xhtml2pdf + Jinja2 | PDF generation |
| requests + ssl + socket | Security scanning |

---

## 📁 Project Structure
Portfolio-SecureAudit/
├── secureaudit-frontend/
│   └── src/
│       ├── components/
│       │   ├── FindingCard.jsx
│       │   ├── Layout.jsx
│       │   ├── LoginForm.jsx
│       │   ├── Navbar.jsx
│       │   ├── RegisterForm.jsx
│       │   ├── ScoreGauge.jsx
│       │   ├── Sidebar.jsx
│       │   └── SeverityBadge.jsx
│       ├── context/
│       │   └── AuthContext.jsx
│       ├── pages/
│       │   ├── AuthPage.jsx
│       │   ├── DashboardPage.jsx
│       │   ├── HistoryPage.jsx
│       │   ├── LandingPage.jsx
│       │   ├── ReportsPage.jsx
│       │   └── ScanPage.jsx
│       ├── services/
│       │   ├── authService.js
│       │   └── scanService.js
│       ├── App.jsx
│       └── main.jsx
│
├── secureaudit-backend/
│   └── app/
│       ├── core/
│       │   ├── config.py
│       │   ├── database.py
│       │   └── security.py
│       ├── models/
│       │   ├── scan.py
│       │   └── user.py
│       ├── routers/
│       │   ├── auth.py
│       │   ├── reports.py
│       │   └── scans.py
│       ├── scanner/
│       │   ├── engine.py
│       │   └── score.py
│       ├── schemas/
│       │   ├── scan.py
│       │   └── user.py
│       ├── templates/
│       │   └── report.html
│       └── main.py
│
└── README.md
---

## 🛠️ Getting Started

### Prerequisites
- Python 3.13+
- Node.js 18+
- PostgreSQL 18

### 1. Clone the repository
```bash
git clone https://github.com/sabyjeany/Portfolio-SecureAudit.git
cd Portfolio-SecureAudit
```

### 2. Setup Backend
```bash
cd secureaudit-backend

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-dotenv pydantic-settings email-validator bcrypt==4.0.1 requests jinja2 xhtml2pdf

# Create .env file
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE secureaudit;"

# Start the server
uvicorn app.main:app --reload
```

### 3. Setup Frontend
```bash
cd secureaudit-frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

### 4. Access the app
- **Frontend** → http://localhost:5173
- **Backend API** → http://localhost:8000
- **API Docs** → http://localhost:8000/docs

---

## 📡 API Documentation

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/auth/register | Create a new account |
| POST | /api/auth/login | Login and get JWT token |
| GET | /api/auth/me | Get current user info |

### Scans
| Method | Endpoint | Description |
|---|---|---|
| POST | /api/scans | Launch a new security scan |
| GET | /api/scans | Get scan history |
| GET | /api/scans/{id} | Get scan details |
| DELETE | /api/scans/{id} | Delete a scan |

### Reports
| Method | Endpoint | Description |
|---|---|---|
| GET | /api/reports/{id} | Download PDF report |

Full interactive documentation available at **http://localhost:8000/docs**

---

## 🛡️ Security Checks

| Check | Severity | Description |
|---|---|---|
| HTTPS | Critical | Does the site use HTTPS? |
| CSP Header | Critical | Content-Security-Policy present? |
| X-Frame-Options | Medium | Protection against clickjacking? |
| X-Content-Type-Options | Medium | Protection against MIME sniffing? |
| HSTS Header | Medium | Strict-Transport-Security present? |
| Referrer-Policy | Low | Referrer information controlled? |
| SSL Certificate | Critical | Certificate valid and not expired? |
| HTTP→HTTPS Redirect | Medium | HTTP redirects to HTTPS? |
| robots.txt | Low | robots.txt file present? |

---

## 👥 Team

| Member | Role | Responsibilities |
|---|---|---|
| Jeany | Frontend / UX | React.js, Tailwind CSS, UI components, PDF integration |
| Yohni | Backend / Cyber | FastAPI, PostgreSQL, Scanner Engine, JWT auth |

---

## 📝 License

This project was built as a portfolio project for educational purposes.

---

*Built with by Jeany & Yohni — SecureAudit 2026*