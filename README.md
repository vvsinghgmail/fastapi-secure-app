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

$ sudo apt update && sudo apt upgrade -y
$ sudo apt install -y build-essential git curl wget unzip

****1.2 Install Docker & Docker Compose****

#### install Docker

$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
$ sudo usermod -aG docker $USER

#### logout/login or `newgrp docker` to apply

##### install docker-compose plugin (modern)

$ sudo apt install -y docker-compose

###### or use Docker Compose v2 plugin: sudo apt-get install docker-compose-plugin

NOTE: containers isolate services (DB, redis, app) and make tear-down/recreate trivial. Docker Compose simplifies multi-service orchestration.

****1.3 Install Python (optional if running in Docker)****

If you plan to run locally or run tests outside container:


****1.4 Install alembic****

$ sudo apt install alembic


# Project Structure
## 1. Folder structure

<img width="763" height="842" alt="image" src="https://github.com/user-attachments/assets/2b01d0e0-6421-428b-926f-e517ea02889f" />


## Clone the repository from Github

GitHub no longer accepts account passwords for git push. You have to use either:

a Personal Access Token (PAT) over HTTPS, or

SSH keys

### Create a Personal Access Token (PAT) on GitHub

#### On your browser:

- Go to GitHub and log in as vvsinghgmail.
- Top-right avatar → Settings.
- Left sidebar → Developer settings → Personal access tokens
- Either “Tokens (classic)” or “Fine-grained tokens”.
- Click Generate new token.
- Give it a name like fastapi-uat-token.
- Expiry: choose something sensible (e.g., 30/90 days).

#### Scopes:

For classic: check at least repo.

Click Generate token.

=> Copy the token somewhere secure (you won’t see it again).

#### Set proper remote & push with token

Set up the remote once, then push:

cd ~/projects/fastapi-secure-app

# set origin (if not already)
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/vvsinghgmail/fastapi-secure-app.git

# check your branch name
git branch:
if main

  git push -u origin main

  else if master then

  git push -u origin master

When it prompts:

Username → vvsinghgmail

Password → paste the token you created (NOT your GitHub password)
---


## Step 1.0 – Make sure you’re in the project root

You should be here:

$ cd ~/projects/fastapi-secure-app
$ ls
# you should see: app/  alembic/  alembic.ini  docker-compose.uat.yml  ...

Step 2.0 – Use a virtual environment (recommended)

If you’re not already using one:

$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt

###Recommended SECRET_KEY (256-bit, URL-safe) in  .env file
You have to change the below line in in  .env file

Recommended SECRET_KEY (256-bit, URL-safe)

Now generate your own (Linux command)

Run this inside your shell:

$ openssl rand -hex 32



Now alembic inside this venv will know about your local packages.

If /usr/bin/alembic still points to system one, you can explicitly run:

python -m alembic revision --autogenerate -m "init"


