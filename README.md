# **Mini-FaaS: A Multi-Runtime Serverless Execution Engine**

## **👨‍💻 The Team: Team Rocket**
* **Team Lead**: Shakti Swaroop Sahoo
* **Team Members**: 
    * Ankita Majhi
    * Rajiv Pradhan
    * Atmananda Behera
    * Nilanchala Mahanty
    
  
**Mini-FaaS** is an asynchronous, polyglot Function-as-a-Service (FaaS) platform built for high-performance code execution in isolated environments. Developed as a 6th-semester CSE skill project at **Indira Gandhi Institute of Technology (IGIT), Sarang**, this system allows users to deploy and execute code snippets in **Python, C, C++, and Java**.

---

## **🚀 Key Features**
* **Multi-Language Support (Polyglot)**: Seamlessly handles interpreted (Python) and compiled (C, C++, Java) languages.
* **Isolated Execution**: Uses **Docker** containers to sandbox code execution, ensuring security and environment consistency.
* **Asynchronous Architecture**: Implements a producer-consumer model using **Redis** and **Background Workers** to handle high-concurrency requests.
* **Persistent Tracking**: All job logs, source code, and execution statuses are stored in a **MySQL** database.
* **Interactive Dashboard**: A user-friendly **Streamlit** frontend for code submission and real-time status polling.

---

## **🏗️ System Architecture**

The system is composed of four main decoupled layers:

1.  **API Layer (FastAPI)**: Serves as the entry point, validating requests and managing the job lifecycle in the database.
2.  **Messaging Layer (Redis)**: A distributed queue that decouples the API from the execution logic, preventing server hangs during heavy compilation tasks.
3.  **Worker Layer (Python)**: A dedicated background process that polls Redis, manages database states, and triggers the executor.
4.  **Sandbox Engine (Docker)**: A custom-built polyglot image containing the `GCC`, `G++`, `OpenJDK`, and `Python3` runtimes.

---

## **🛠️ Tech Stack**
| Component | Technology Used |
| :--- | :--- |
| **Frontend** | Streamlit |
| **Backend API** | FastAPI |
| **Database** | MySQL (SQLAlchemy ORM) |
| **Task Queue** | Redis |
| **Containerization**| Docker |
| **Languages** | Python, C++, C, Java |

---

## **📂 Project Structure**
```text
Mini_FAAS/
├── api/
│   ├── main.py          # FastAPI routes & logic
│   ├── models.py        # SQLAlchemy database schemas
│   └── database.py      # MySQL connection setup
├── core/
│   ├── executor.py      # Docker execution logic
│   └── queue.py         # Redis producer logic
├── worker/
│   └── worker.py        # Background task consumer
├── Schema/
│   ├── job.py           # Pydantic request/response models
│   └── __init__.py      # Schema exports
├── frontend/
│   └── app.py           # Streamlit dashboard
└── docker-compose.yml   # Infrastructure orchestration
