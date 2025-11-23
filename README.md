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
