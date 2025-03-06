# K8s AI Monitor API

API for monitoring Kubernetes clusters with AI-powered incident detection and analysis.

## Features

- Track and manage Kubernetes incidents
- Store and analyze logs and events
- AI-powered diagnosis and recommendations
- Notification tracking for incidents

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
fastapi dev main.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Database

The application uses SQLite with SQLAlchemy ORM. The database file is created at `k8s_monitor.db`.
