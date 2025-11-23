# fastapi-secure-app
full FastAPI + SQLModel project scaffold


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

****1.1 Update OS & install base tools:

sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential git curl wget unzip

****1.2 Install Docker & Docker Compose

#### install Docker

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

#### logout/login or `newgrp docker` to apply

##### install docker-compose plugin (modern)
sudo apt install -y docker-compose
###### or use Docker Compose v2 plugin: sudo apt-get install docker-compose-plugin

NOTE: containers isolate services (DB, redis, app) and make tear-down/recreate trivial. Docker Compose simplifies multi-service orchestration.

****1.3 Install Python (optional if running in Docker)

If you plan to run locally or run tests outside container:

