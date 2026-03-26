# User Management API

REST API for user management with role-based access control, event-driven messaging via Kafka, and a retry/dead-letter queue system.

## Features

- JWT authentication — register, login, token-based access (1h expiry)
- Role-based access control: `admin` and `user` roles
- Admins can create, read, update, delete, activate/deactivate, and change roles of any user
- Users can read and update their own profile
- Kafka event queue — publishes `UserRegistered` events on every registration
- Retry queue with exponential backoff (10s → 30s → 60s) and dead-letter queue (DLQ)
- Interactive API docs (Swagger UI) at `/docs`
- Structured request logging with timing
- SOLID architecture: Repository pattern, Service layer, Dependency Inversion

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Flask 3 + flask-smorest (OpenAPI 3) |
| Database | PostgreSQL 15 via SQLAlchemy |
| Auth | Flask-JWT-Extended (Bearer tokens) |
| Validation | Marshmallow schemas |
| Messaging | Apache Kafka 3.7 (KRaft — no Zookeeper) |
| Production server | Gunicorn |
| Containers | Docker + Docker Compose |

---

## Running with Docker

This is the recommended way to run everything — API, database, Kafka, and the consumer worker all start together.

### 1. Start all services

```bash
docker compose up --build
```

This will:
1. Start PostgreSQL and wait until healthy
2. Start Kafka (KRaft mode) and wait until healthy
3. Run `kafka-init` to create the three topics
4. Start the Flask API on `http://localhost:5000`
5. Start the consumer `worker` that listens on `users.registered` and `users.registered.retry`

### 2. Create your first admin user

In a separate terminal, while the containers are running:

```bash
docker compose exec web flask create-admin
```

You will be prompted for a username, email, and password.

### 3. Open the API docs

```
http://localhost:5000/docs
```

Click **Authorize** in the top-right, paste your token from `/auth/login`, and explore all endpoints interactively.

### Useful Docker commands

```bash
# Run in background
docker compose up --build -d

# View logs for a specific service
docker compose logs -f web
docker compose logs -f worker
docker compose logs -f kafka

# Stop everything
docker compose down

# Stop and wipe all data (database + Kafka)
docker compose down -v

# Restart only the worker
docker compose restart worker
```

---

## Running Locally (without Docker)

You need a running PostgreSQL instance. Kafka is optional — the API falls back gracefully when `KAFKA_BOOTSTRAP_SERVERS` is not set.

### 1. Activate the virtual environment

```bash
# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

```bash
# Windows (PowerShell)
$env:FLASK_APP = "main.py"
$env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/userdb"

# macOS / Linux
export FLASK_APP=main.py
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/userdb
```

Copy `.env.example` to `.env` and fill in values if you prefer a file-based approach.

### 4. Create database tables

```bash
flask init-db
```

### 5. Start the API

```bash
flask run
```

### 6. (Optional) Start the Kafka worker

Only needed if you have Kafka running locally:

```bash
export KAFKA_BOOTSTRAP_SERVERS=localhost:9094
python worker.py
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:postgres@localhost:5432/userdb` |
| `SECRET_KEY` | Flask session secret key | `dev-secret-key-change-in-production` |
| `JWT_SECRET_KEY` | JWT signing key | `jwt-secret-key-change-in-production` |
| `FLASK_APP` | Flask entry point | `main.py` |
| `FLASK_ENV` | `development` uses Flask dev server; `production` uses Gunicorn | `development` |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address (e.g. `kafka:9092`). If not set, events are silently skipped | — |

---

## CLI Commands

```bash
flask init-db          # Create all database tables
flask create-admin     # Interactive prompt to create an admin user
```

---

## API Endpoints

Full interactive docs at `http://localhost:5000/docs`.

### Auth

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/auth/register` | Public | Register a new user |
| `POST` | `/auth/login` | Public | Login — returns a JWT `access_token` |
| `GET` | `/auth/me` | Authenticated | Get own profile |

### Users

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/users/` | Admin | List all users |
| `GET` | `/users/<id>` | Admin or self | Get user by ID |
| `PUT` | `/users/<id>` | Admin or self | Update username, email, or password. Role change: admin only |
| `DELETE` | `/users/<id>` | Admin | Delete a user (cannot delete yourself) |
| `PATCH` | `/users/<id>/role` | Admin | Change role to `admin` or `user` (cannot change your own) |
| `PATCH` | `/users/<id>/status` | Admin | Set `is_active` to `true` or `false` (cannot change your own) |

### How to authenticate

1. Call `POST /auth/login` with `{"username": "...", "password": "..."}`
2. Copy the `access_token` from the response
3. Add it to every protected request:

```
Authorization: Bearer <access_token>
```

### Example flow

```bash
# Register
curl -X POST http://localhost:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "mypassword"}'

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "mypassword"}'

# Get own profile (replace TOKEN)
curl http://localhost:5000/auth/me \
  -H "Authorization: Bearer TOKEN"

# List all users (admin only)
curl http://localhost:5000/users/ \
  -H "Authorization: Bearer TOKEN"
```

---

## Kafka & Event Queue

Every successful user registration publishes a `UserRegistered` event to Kafka.

### Topics

| Topic | Partitions | Description |
|---|---|---|
| `users.registered` | 3 | Main topic — new registration events |
| `users.registered.retry` | 1 | Failed messages, re-queued with retry count |
| `users.registered.dlq` | 1 | Dead-letter queue — messages that failed all retries |

### Retry strategy

When a consumer fails to process a message, it is re-published to the retry topic with a `retry-count` header. The retry consumer sleeps before processing based on the attempt number:

| Attempt | Delay |
|---|---|
| 1 | 10 seconds |
| 2 | 30 seconds |
| 3 | 60 seconds |
| 4+ | → Dead-letter queue |

### Message format

```json
{
  "user_id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "registered_at": "2024-01-15T10:30:00+00:00"
}
```

### Inspecting topics (inside Docker)

```bash
# List topics
docker compose exec kafka /opt/bitnami/kafka/bin/kafka-topics.sh \
  --bootstrap-server localhost:9092 --list

# Consume messages from the main topic
docker compose exec kafka /opt/bitnami/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic users.registered --from-beginning

# Inspect the DLQ
docker compose exec kafka /opt/bitnami/kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic users.registered.dlq --from-beginning
```

Connect from your host machine on port `9094` (mapped by Docker Compose):

```bash
kafka-console-consumer.sh --bootstrap-server localhost:9094 \
  --topic users.registered --from-beginning
```

---

## Running Tests

Tests use an in-memory SQLite database — no external services required.

```bash
pip install pytest pytest-cov
pytest --cov=app
```

Run a single test file:

```bash
pytest tests/test_auth.py -v
```

---

## Linting

```bash
pip install flake8
flake8 app/ main.py worker.py
```

Configuration is in `.flake8` (max line length: 100).

---

## Deployment (Render)

`render.yaml` defines the full infrastructure as code.

1. Push this repository to GitHub
2. Go to [render.com](https://render.com) → **New > Blueprint**
3. Connect your GitHub repository
4. Render reads `render.yaml` and automatically provisions:
   - Web service (Docker, Gunicorn)
   - Managed PostgreSQL database
   - Injects `DATABASE_URL`, `SECRET_KEY`, `JWT_SECRET_KEY` automatically

5. After the first deploy, open the Render shell and create an admin:

```bash
flask create-admin
```

> **Note:** The Render free tier does not include Kafka. To use the event queue in production, connect an external Kafka provider (Confluent Cloud, Upstash Kafka, etc.) and set `KAFKA_BOOTSTRAP_SERVERS`. Without it, the API works fully — events are silently skipped via `NullEventProducer`.

---

## Architecture

```
app/
  kafka/
    topics.py           # Topic name constants
    events.py           # UserRegisteredEvent + AbstractEventProducer + NullEventProducer
    producer.py         # KafkaEventProducer (publishes events; failures logged, not re-raised)
    consumer.py         # BaseConsumer ABC with retry logic, backoff, and DLQ routing
  consumers/
    user_consumer.py    # UserRegistrationConsumer + UserRegistrationRetryConsumer
  repositories/
    base.py             # AbstractUserRepository interface (ABC)
    user_repository.py  # SQLAlchemy implementation
  services/
    exceptions.py       # ServiceError — single exception type for all service errors
    user_service.py     # UserService — CRUD business logic
    auth_service.py     # AuthService — register, login, publishes Kafka event
  routes/
    auth.py             # /auth endpoints
    users.py            # /users endpoints
  __init__.py           # App factory
  config.py             # Environment-based configuration
  logger.py             # Structured logging + request timing middleware
  models.py             # User model + Role constants
  providers.py          # Dependency injection — wires repos, services, and event producer
  schemas.py            # Marshmallow schemas per operation
main.py                 # Flask entry point + CLI commands
worker.py               # Consumer worker — two threads (main + retry)
```

### SOLID principles

| Principle | How it's applied |
|---|---|
| **Single Responsibility** | Repository = data access only. Service = business logic only. Route = HTTP only. |
| **Open/Closed** | New event types or user operations extend via new classes, not by modifying existing ones. |
| **Liskov Substitution** | `UserRepository` can replace `AbstractUserRepository` anywhere without changing behavior. |
| **Interface Segregation** | One Marshmallow schema per operation — `RegisterSchema`, `UpdateUserSchema`, `RoleSchema`, etc. |
| **Dependency Inversion** | `AuthService` depends on `AbstractEventProducer`; `UserService` depends on `AbstractUserRepository`. Concrete implementations are injected via `providers.py`. |
