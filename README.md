# 🚀 FastAPI Core Concept Study for Data Engineers

Consuming and exposing APIs is a regular task in a Data Engineer's routine. To build a rock-solid foundation in Python and backend communications, I took the initial 7 hours of the [freeCodeCamp.org 19 hours FastAPI course](https://www.youtube.com/watch?v=0sOvCWFmrtA&t=28285s). 

This repository serves as a hands-on proof of concept covering the crucial backend architectures that every data professional must understand to handle ingestion pipelines and analytical data exposure properly.

---

## 🏗️ Project Architecture & File Structure

The project was refactored into a scalable modular package layout, isolating routers, models, database configs, and utilities.

- **app/routers/**: Split endpoint logic into dedicated routers (`auth`, `post`, `user`).
- **db.py**: Establishes database communication and dependency injections (`get_db`).
- **models.py**: Defines PostgreSQL relational database schemas via ORM mapped classes.
- **schemas.py**: Handles strict request data validation and structured response objects using Pydantic.
- **oauth2.py / auth.py**: Directs the security payload logic and token verification.
- **utils.py**: Centralizes general helper methods like password hashing.

---

## 🛠️ Tech Stack & Key Concepts Mastered

During this initial sprint, I focused heavily on data validation, relational persistence, and security protocols:

*   **FastAPI**: Implemented structured path operations, automatic documentation generation (`/docs` and `/redoc`), and clean query parameters.
*   **PostgreSQL**: Handled complex data types, entity schemas, constraints (primary keys, foreign keys, not-null constraints), and deep relational operations.
*   **SQLAlchemy (ORM)**: Decoupled raw database connection dependencies using Python objects, mapping schemas directly to live database states.
*   **Pydantic**: Created explicit data type boundaries for validation, separating strictly what the endpoint receives from what it exposes back to the client.
*   **JWT & OAuth2**: Locked down sensitive pathways by integrating JSON Web Token encryption with the `OAuth2PasswordRequestForm` dependency workflow.
*   **Postman**: Utilized as a rigorous interface testing playground to build custom request collections, payloads, dynamic environment variables, and authentication testing headers.

---

## 🎯 Data Engineering Context: Why This Matters
Instead of just deploying a simple social backend application, understanding these concepts allowed me to master:
1. **API Ingestion Scenarios:** Knowing how external systems validate their formats through schemas so we can fetch/parse JSON streams error-free.
2. **Exposing Data Assets:** Building high-performance, validated endpoints to serve computed entities out of Data Lakes or Analytical Warehouses securely to analytics dashboards or data scientists.

---
## ⚡ How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/CAPTURACERTA/python_api_development
   ```
2. Create and activate your virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/env/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create your local database environment variables file (`.env`).
5. Spin up the server:
   ```bash
   uvicorn app.main:app --reload
   ```
6. Head over to `http://127.0.0` to interactive test with the automated Swagger UI!
