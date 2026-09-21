SIDORA AI - MLOps Platform Documentation
=========================================

Welcome to the documentation for the **SIDORA AI MLOps Microservices Platform**.

Architecture Overview
---------------------

The platform transforms ML algorithms into an enterprise-grade, containerized software product:

* **FastAPI Backend (`app_api`)**: RESTful API managing text persistence, data validation, and health checks.
* **Streamlit Frontend (`app_front`)**: Multi-page dashboard interface for user interaction and data visualization.
* **PostgreSQL Database (`db`)**: Persistent relational storage isolated within the internal Docker network.
* **Docker Compose Orchestration**: Segregated networks (`front-api`, `api-db`) ensuring strict database isolation.
* **CI/CD & Security**: Automated GitHub Actions pipelines covering Ruff linting, Gitleaks secret detection, and Pytest coverage (>80%).

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   modules

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
