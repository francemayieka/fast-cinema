# Fast Cinema: Movie Dashboard

A secure, data-rich dashboard built with FastAPI and PostgreSQL, leveraging environment variables for configuration. The application uses psycopg2 as the PostgreSQL adapter for efficient and secure database connectivity in Python.

## Prerequisites

Dependencies: Install all required Python packages using the requirements.txt file:

```bash
pip install -r requirements.txt
```

Configuration: Create a file named `.env` in the root directory and add your PostgreSQL connection string:

```
DATABASE_URL='your_full_connection_string_here'
```

## To Run the Dashboard

Use uvicorn to start the FastAPI server:

```bash
uvicorn main:app --reload
```

Once running, the dashboard will be accessible at http://127.0.0.1:8000/.