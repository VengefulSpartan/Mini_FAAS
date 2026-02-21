# 🚀 Mini-FaaS Engine

A lightweight, Python-based Function-as-a-Service (FaaS) platform built from scratch. This system allows users to deploy and execute Python scripts in isolated Docker containers via a seamless web dashboard, mimicking the core behavior of AWS Lambda.

## 📌 Overview
The goal of Phase 1 (The "Walking Skeleton") is to establish a robust, end-to-end event-driven architecture. 
**Flow:** `User UI` $\rightarrow$ `API Gateway` $\rightarrow$ `Redis Queue` $\rightarrow$ `Background Worker` $\rightarrow$ `Docker Executor` $\rightarrow$ `Database` $\rightarrow$ `User UI`.

## 🛠 Tech Stack
* **Language:** Python 3.12
* **Frontend:** Streamlit
* **API Gateway:** FastAPI
* **Message Broker:** Redis
* **Execution Engine:** Docker SDK (Python)
* **Database:** SQLite (SQLAlchemy ORM)

---

## 👥 Team Roster & Module Ownership

This is a Monorepo. Please strictly work within your designated module to avoid merge conflicts.

| Name       | Role | Module / Directory | Responsibility |
|:-----------| :--- | :--- | :--- |
| **Shakti** | Architect & Backend | `api/` & `schemas/` | FastAPI gateway, Database models, System Schemas, Integration. |
| **Rajiv**  | The Executioner | `core/executor.py` | Docker SDK logic, container lifecycle, and secure execution. |
| **Ankit**  | The Producer | `core/queue.py` | Redis setup and queue pushing logic. |
| **Nila**   | The Consumer | `worker/` | The background worker loop, pulling jobs, and triggering executions. |
| **Ankita** | The Frontend | `frontend/` | Streamlit user dashboard and API polling logic. |

---

## 📂 Repository Structure

```text
mini-faas/
├── api/                # FastAPI endpoints and database logic
├── core/               # Shared engine logic (Docker & Redis)
├── frontend/           # Streamlit UI dashboard
├── schemas/            # ⚠️ THE CONTRACTS: Shared Pydantic models
├── worker/             # Background task processor
├── docker-compose.yml  # Infrastructure setup
├── requirements.txt    # Python dependencies
└── README.md