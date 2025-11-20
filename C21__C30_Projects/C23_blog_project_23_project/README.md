# 📝 Blog API Project

<div align="center">

![Django](https://img.shields.io/badge/Django-5.2.8-092E20?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Latest-009639?style=for-the-badge&logo=nginx&logoColor=white)

**Django-based RESTful blog API with Django Ninja framework**

[Features](#-features) • [Installation](#-installation) • [API Docs](#-api-endpoints) • [Testing](#-testing)

</div>

---

## 🎯 Overview

Modern blog API built with Django Ninja, featuring JWT authentication, article management, commenting system, and comprehensive logging. Fully containerized with Docker and production-ready with Nginx reverse proxy.

## 🚀 Tech Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Backend** | Django | 5.2.8 | Web framework |
| **API** | Django Ninja | 1.4.5 | Fast API framework |
| **Database** | PostgreSQL | 15 | Production database |
| **Database** | SQLite | 3 | Development database |
| **Auth** | Django Ninja JWT | 5.4.0 | JWT authentication |
| **Server** | Gunicorn | 21.2.0 | WSGI HTTP server |
| **Proxy** | Nginx | Alpine | Reverse proxy |
| **Containerization** | Docker | Latest | Container platform |
| **Testing** | Pytest | 9.0.1 | Testing framework |
| **Admin** | Jazzmin | 3.0.1 | Modern admin interface |

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔐 Authentication & Authorization
- ✅ User registration with validation
- ✅ JWT token authentication (access + refresh)
- ✅ Custom token system
- ✅ Secure password hashing
- ✅ Token expiration management
- ✅ Logout functionality

</td>
<td width="50%">

### 📰 Article Management
- ✅ Create, read, update, delete articles
- ✅ User ownership validation
- ✅ Automatic timestamps
- ✅ Author association
- ✅ Rich content support
- ✅ Pagination ready

</td>
</tr>
<tr>
<td width="50%">

### 💬 Comment System
- ✅ Add comments to articles
- ✅ Edit own comments
- ✅ Delete own comments
- ✅ Comment-article relationship
- ✅ Author tracking
- ✅ Chronological ordering

</td>
<td width="50%">

### 🛠️ Additional Features
- ✅ Admin panel with Jazzmin
- ✅ Comprehensive logging
- ✅ Error handling
- ✅ User profiles with bio & avatar
- ✅ Multiple environment configs
- ✅ Docker deployment ready

</td>
</tr>
</table>

## 📂 Project Structure

```
C23_blog_project/
│
├── 📱 apps/
│   ├── blog/                   # Blog application
│   │   ├── api.py             # Blog API endpoints
│   │   ├── models.py          # Article & Comment models
│   │   ├── serializers.py     # Pydantic schemas
│   │   ├── admin.py           # Admin configuration
│   │   └── tests.py           # Unit tests
│   │
│   └── users/                  # User management
│       ├── api.py             # Auth endpoints
│       ├── models.py          # User models
│       ├── serializers.py     # User schemas
│       └── tests/             # Test suite
│
├── ⚙️ core/
│   ├── settings/
│   │   ├── base.py           # Base configuration
│   │   ├── dev.py            # Development settings
│   │   ├── prod.py           # Production settings
│   │   └── testing.py        # Test configuration
│   └── urls.py               # URL routing
│
├── 🐳 Docker files
│   ├── docker-compose.yml     # Service orchestration
│   ├── Dockerfile            # Application image
│   ├── nginx.conf            # Nginx configuration
│   └── entrypoint.sh         # Container startup script
│
└── 📋 Configuration
    ├── requirements.txt       # Python dependencies
    ├── .env                  # Environment variables
    └── .dockerignore         # Docker ignore rules
```

## 🔧 Installation

### 🖥️ Local Development (SQLite)

<table>
<tr>
<td width="30%"><strong>Step 1</strong></td>
<td width="70%">

**Clone repository**
```bash
git clone https://github.com/Islam0122/99_pet_projects_backend.git
cd C23_blog_project
```
</td>
</tr>
<tr>
<td><strong>Step 2</strong></td>
<td>

**Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
</td>
</tr>
<tr>
<td><strong>Step 3</strong></td>
<td>

**Install dependencies**
```bash
pip install -r requirements.txt
```
</td>
</tr>
<tr>
<td><strong>Step 4</strong></td>
<td>

**Run migrations**
```bash
python manage.py migrate
python manage.py createsuperuser
```
</td>
</tr>
<tr>
<td><strong>Step 5</strong></td>
<td>

**Start server**
```bash
python manage.py runserver
```
🌐 API: `http://127.0.0.1:8000/api/`
</td>
</tr>
</table>

### 🐳 Production (Docker + PostgreSQL)

<table>
<tr>
<td width="30%"><strong>Step 1</strong></td>
<td width="70%">

**Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```
</td>
</tr>
<tr>
<td><strong>Step 2</strong></td>
<td>

**Build and run**
```bash
docker-compose up -d --build
```
</td>
</tr>
<tr>
<td><strong>Step 3</strong></td>
<td>

**Access services**
- 🌐 API: `http://localhost/api/`
- 👤 Admin: `http://localhost/admin/`
- 📖 Docs: `http://localhost/api/docs`
</td>
</tr>
</table>

## 🔌 API Endpoints

### 🔐 Authentication Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/users/register` | ❌ | Register new user (JWT) |
| `POST` | `/api/users/login` | ❌ | Login user (JWT) |
| `POST` | `/api/users/register-custom` | ❌ | Register with custom token |
| `POST` | `/api/users/login-custom` | ❌ | Login with custom token |
| `POST` | `/api/users/logout-custom` | ✅ Custom | Logout (invalidate token) |

### 👤 Profile Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `GET` | `/api/users/profile` | ✅ JWT | Get current user profile |
| `PUT` | `/api/users/profile` | ✅ JWT | Update user profile |
| `GET` | `/api/users/profile-custom` | ✅ Custom | Get profile (custom token) |

### 📰 Article Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/blog/articles` | ✅ JWT | Create new article |
| `GET` | `/api/blog/articles` | ❌ | List all articles |
| `GET` | `/api/blog/articles/{id}` | ❌ | Get specific article |
| `PUT` | `/api/blog/articles/{id}` | ✅ JWT (Owner) | Update article |
| `DELETE` | `/api/blog/articles/{id}` | ✅ JWT (Owner) | Delete article |

### 💬 Comment Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| `POST` | `/api/blog/comments` | ✅ JWT | Create new comment |
| `GET` | `/api/blog/comments/{article_id}` | ❌ | List article comments |
| `PUT` | `/api/blog/comments/{id}` | ✅ JWT (Owner) | Update comment |
| `DELETE` | `/api/blog/comments/{id}` | ✅ JWT (Owner) | Delete comment |

## 📝 API Usage Examples

### Registration & Login

<table>
<tr>
<td width="50%">

**JWT Registration**
```bash
POST /api/users/register
Content-Type: application/json

{
  "username": "johndoe",
  "password": "secure123",
  "email": "john@example.com"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1Qi...",
  "refresh": "eyJ0eXAiOiJKV1Qi..."
}
```

</td>
<td width="50%">

**Custom Token Login**
```bash
POST /api/users/login-custom
Content-Type: application/json

{
  "username": "johndoe",
  "password": "secure123"
}
```

**Response:**
```json
{
  "token": "abc123xyz...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  }
}
```

</td>
</tr>
</table>

### Article Management

<table>
<tr>
<td width="50%">

**Create Article**
```bash
POST /api/blog/articles
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My First Article",
  "content": "Article content..."
}
```

</td>
<td width="50%">

**Update Article**
```bash
PUT /api/blog/articles/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content..."
}
```

</td>
</tr>
</table>

### Comment Operations

<table>
<tr>
<td width="50%">

**Add Comment**
```bash
POST /api/blog/comments
Authorization: Bearer <token>
Content-Type: application/json

{
  "article_id": 1,
  "content": "Great article!"
}
```

</td>
<td width="50%">

**List Comments**
```bash
GET /api/blog/comments/1

Response:
[
  {
    "id": 1,
    "article_id": 1,
    "author_id": 2,
    "content": "Great!",
    "created_at": "2025-01-15T..."
  }
]
```

</td>
</tr>
</table>

## 📊 Database Schema

### User Models

| Model | Fields | Description |
|-------|--------|-------------|
| **User** | id, username, email, password | Django default user model |
| **UserProfile** | user, bio, avatar, created_at, updated_at | Extended user information |
| **UserToken** | user, token, created_at, expires_at, is_active | Custom authentication tokens |

### Blog Models

| Model | Fields | Description |
|-------|--------|-------------|
| **Article** | id, author, title, content, created_at, updated_at | Blog posts |
| **Comment** | id, article, author, content, created_at, updated_at | Article comments |

### Relationships

```
User (1) ──── (N) Article
User (1) ──── (N) Comment
Article (1) ──── (N) Comment
User (1) ──── (1) UserProfile
User (1) ──── (N) UserToken
```

## 🧪 Testing

### Test Coverage Summary

| Category | Tests | Status |
|----------|-------|--------|
| **User Registration** | JWT & Custom token registration | ✅ |
| **User Login** | JWT & Custom token login | ✅ |
| **User Profile** | Get/Update profile operations | ✅ |
| **Token Management** | Token generation & validation | ✅ |
| **Article CRUD** | Create, Read, Update, Delete | ✅ |
| **Comment CRUD** | Create, Read, Update, Delete | ✅ |
| **Authorization** | Owner-only edit/delete | ✅ |
| **Model Methods** | Token generation, string repr | ✅ |

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.blog

# Run with pytest
pytest

# Run with coverage
pytest --cov=apps --cov-report=html
```

### Test Structure

```
apps/users/tests/
├── test_registration.py    # Registration tests
├── test_login.py           # Login tests
├── test_profile.py         # Profile tests
├── test_custom_token.py    # Custom token tests
└── test_models.py          # Model tests

apps/blog/
└── tests.py               # Article & Comment tests
```

## 📝 Logging Configuration

### Development Environment

| Log Level | File | Content |
|-----------|------|---------|
| **ERROR** | `logs/error.log` | Application errors, exceptions |
| **WARNING** | `logs/warning.log` | Failed auth attempts, unauthorized access |
| **INFO** | `logs/info.log` | User actions, CRUD operations |
| **Console** | stdout | All levels for development |

### Production Environment

| Log Level | File | Settings |
|-----------|------|----------|
| **ERROR** | `/var/log/django/error.log` | Max 10MB, 5 backups |
| **WARNING** | `/var/log/django/warning.log` | Max 10MB, 5 backups |
| **INFO** | `/var/log/django/info.log` | Max 10MB, 5 backups |

### Logged Events

✅ User registration/login/logout  
✅ Article create/update/delete  
✅ Comment create/update/delete  
✅ Authentication failures  
✅ Authorization violations  
✅ API errors and exceptions  

## 🐳 Docker Management

### Essential Commands

| Command | Description |
|---------|-------------|
| `docker-compose up -d --build` | Build and start all services |
| `docker-compose down` | Stop all services |
| `docker-compose down -v` | Stop and remove volumes (⚠️ deletes data) |
| `docker-compose logs -f web` | View web service logs |
| `docker-compose exec web python manage.py migrate` | Run migrations |
| `docker-compose exec web python manage.py createsuperuser` | Create admin user |
| `docker-compose ps` | List running services |
| `docker-compose restart web` | Restart web service |

### Container Architecture

```
┌─────────────────┐
│   Nginx:80      │  ← Reverse Proxy
└────────┬────────┘
         │
┌────────▼────────┐
│  Django:8000    │  ← Web Application
└────────┬────────┘
         │
┌────────▼────────┐
│ PostgreSQL:5432 │  ← Database
└─────────────────┘
```

## ⚙️ Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DJANGO_ENV` | `dev` | Environment mode: `dev`, `prod`, `testing` |
| `SECRET_KEY` | - | Django secret key (⚠️ change in production) |
| `POSTGRES_DB` | `blog_db` | Database name |
| `POSTGRES_USER` | `blog_user` | Database user |
| `POSTGRES_PASSWORD` | - | Database password (⚠️ required) |
| `POSTGRES_HOST` | `db` | Database host |
| `POSTGRES_PORT` | `5432` | Database port |

## 🔒 Security Features

| Feature | Implementation |
|---------|---------------|
| **Password Security** | Django's PBKDF2 algorithm with SHA256 |
| **Token Security** | JWT with 24h expiration, Custom tokens with deactivation |
| **CSRF Protection** | Django middleware enabled |
| **SQL Injection** | Django ORM parameterized queries |
| **XSS Protection** | Django template auto-escaping |
| **Ownership Validation** | User-based authorization checks |
| **Input Validation** | Pydantic schema validation |

## 🎨 Admin Panel

**Access:** `http://localhost/admin/`

**Features:**
- 🎨 Modern Jazzmin interface
- 👥 User management with token preview
- 📰 Article moderation with filters
- 💬 Comment management
- 🔍 Advanced search and filtering
- 📊 Statistics dashboard

## 🚀 Production Deployment Checklist

- [ ] Change `SECRET_KEY` to secure random value
- [ ] Update `POSTGRES_PASSWORD` in `.env`
- [ ] Configure `ALLOWED_HOSTS` for your domain
- [ ] Set up SSL certificates (Let's Encrypt)
- [ ] Enable HTTPS in Nginx configuration
- [ ] Configure database backups
- [ ] Set up monitoring (e.g., Sentry)
- [ ] Configure log rotation
- [ ] Test all endpoints
- [ ] Run security audit
- [ ] Document deployment process

## 📚 Additional Resources

| Resource | Link |
|----------|------|
| **Django** | [docs.djangoproject.com](https://docs.djangoproject.com/) |
| **Django Ninja** | [django-ninja.rest-framework.com](https://django-ninja.rest-framework.com/) |
| **Django Ninja JWT** | [github.com/eadwinCode/django-ninja-jwt](https://github.com/eadwinCode/django-ninja-jwt) |
| **PostgreSQL** | [postgresql.org/docs](https://www.postgresql.org/docs/) |
| **Docker** | [docs.docker.com](https://docs.docker.com/) |
