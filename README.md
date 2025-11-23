# fastapi-secure-app
full FastAPI + SQLModel project scaffold

Below is a full FastAPI + SQLModel project scaffold with:

1. Secure user registration & login
2. Access + Refresh tokens (rotation + revocation)
3. Role-based auth (Admin/User)
4. Blog CRUD
5. DB-level validations
6. Token-based session management via refresh tokens
7. OAuth2 Bearer protection
8. UAT setup: Docker Compose, .env.uat, seed script, and workflow

I’ll assume you’ll put this in a folder called: fastapi-secure-app and then push it to your own GitHub.


**Pre-req decisions & rationale (short)**

- OS: Ubuntu 22.04 LTS or 24.04 LTS — stable, widely supported for servers and CI/CD.
- Containerization: Docker + Docker Compose — reproducible environments for UAT and easy parity with production.
- Python: 3.11+ recommended (stable, good Pydantic/SQLAlchemy support). Use virtualenv for local installs. 
- DB: PostgreSQL (production-grade; strong constraints, rich features).  
- Cache/session store: Redis (stores refresh tokens, blacklists, rate-limit counters)
- ASGI server: Uvicorn for dev / lightweight UAT; in production pair with Gunicorn+Uvicorn workers or a process manager.  

**Rationale** 
this stack balances developer ergonomics, performance, and security. Docker gives reproducible infrastructure; PostgreSQL + SQLAlchemy/SQLModel provides reliable constraints and migrations.

**Procedure**
***Prepare the UAT machine (Ubuntu example)***

****1.1 Update OS & install base tools:****

sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl wget unzip

****1.2 Install Docker & Docker Compose****

#### install Docker

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

#### logout/login or `newgrp docker` to apply

##### install docker-compose plugin (modern)
sudo apt install -y docker-compose
###### or use Docker Compose v2 plugin: sudo apt-get install docker-compose-plugin

NOTE: containers isolate services (DB, redis, app) and make tear-down/recreate trivial. Docker Compose simplifies multi-service orchestration.

****1.3 Install Python (optional if running in Docker)****

If you plan to run locally or run tests outside container:


# Project Structure
## 1. Folder structure

fastapi-secure-app
├── alembic
│   └── env.py
├── alembic.ini
├── app
│   ├── api
│   │   ├── deps.py
│   │   └── v1
│   │       ├── auth.py
│   │       └── blogs.py
│   ├── core
│   │   ├── config.py
│   │   └── security.py
│   ├── db
│   │   └── session.py
│   ├── main.py
│   ├── models
│   │   ├── blog.py
│   │   ├── token.py
│   │   └── user.py
│   └── schemas
│       ├── auth.py
│       ├── blog.py
│       └── user.py
├── docker-compose.uat.yml
├── README.md
├── requirements.txt
├── scripts
│   └── seed_uat.py
└── tests
    └── test_auth.py


