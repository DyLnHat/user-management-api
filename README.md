# User Management API

REST API for user management with roles and JWT authentication, built with FastAPI, PostgreSQL and Docker.

---

## Tech Stack

- **FastAPI** — Web framework with automatic Swagger docs
- **SQLModel** — ORM combining SQLAlchemy + Pydantic
- **PostgreSQL** — Relational database
- **Alembic** — Database migrations
- **JWT** — Authentication with expiration
- **bcrypt** — Password hashing
- **Docker + Docker Compose** — Containerization
- **Pytest** — Testing

---

## Project Structure

```
user-management-api/
├── app/
│   ├── api/v1/          # Routes (auth, users)
│   ├── core/            # Config, security, dependencies
│   ├── db/              # Database connection and session
│   ├── models/          # SQLModel models
│   ├── repositories/    # Database queries
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   └── main.py          # Entry point
├── migrations/          # Alembic migrations
├── tests/               # Pytest tests
├── .env.example         # Environment variables template
├── Dockerfile
└── docker-compose.yml
```

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/)
- [Docker Compose](https://docs.docker.com/compose/)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/user-management-api.git
cd user-management-api
```

### 2. Configure environment variables

```bash
copy .env.example .env  # Windows
cp .env.example .env # Mac/Linux
```

Edit `.env` with your values:

```env
DATABASE_URL=postgresql://admin:secret@db:5432/userdb
POSTGRES_USER=admin
POSTGRES_PASSWORD=secret
POSTGRES_DB=userdb
SECRET_KEY=your-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 3. Start the application

```bash
docker compose up --build
```

The API will be available at **http://localhost:8000**

Migrations run automatically on startup.

---

## API Documentation

Interactive docs available at:

- **Swagger UI** → http://localhost:8000/docs
- **ReDoc** → http://localhost:8000/redoc

---

## Endpoints

### Auth

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register a new user | No |
| POST | `/api/v1/auth/login` | Login and get JWT token | No |

### Users

| Method | Endpoint | Description | Role required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/users/` | List all users | user |
| GET | `/api/v1/users/me` | Get current user | user |
| GET | `/api/v1/users/{id}` | Get user by ID | user |
| PATCH | `/api/v1/users/{id}` | Update user | admin |
| DELETE | `/api/v1/users/{id}` | Delete user | admin |

### Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |

---

## Usage Example

### Register a user

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword",
    "full_name": "John Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Use protected endpoint

```bash
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer your-token-here"
```

---

## Running Tests

### Local

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

---

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/db` |
| `POSTGRES_USER` | PostgreSQL username | `admin` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `secret` |
| `POSTGRES_DB` | PostgreSQL database name | `userdb` |
| `SECRET_KEY` | JWT signing key | `your-secret-key` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT expiration in minutes | `30` |

> ⚠️ Never commit your `.env` file! Use `.env.example` as a template.

---

## Design Decisions

- **No logic in controllers** — routes only receive requests and call services
- **Repository pattern** — database queries are isolated from business logic
- **Service layer** — all business logic lives in services
- **No hardcoded credentials** — everything via environment variables
- **Controlled errors** — all exceptions are caught and return proper HTTP status codes

---

## License

MIT
