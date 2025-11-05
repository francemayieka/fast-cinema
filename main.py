from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import psycopg2
from contextlib import contextmanager
import os
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from .env file
load_dotenv()
# Retrieve the connection string from environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# Check if the URL was loaded (a quick safety check)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file or environment variables!")

app = FastAPI(title="Movie Dashboard")
# Set up Jinja2 templates directory
templates = Jinja2Templates(directory="templates")

# --- Database Connection Management ---
@contextmanager
def get_db_cursor():
    """A context manager to handle PostgreSQL connection and cursor."""
    conn = None
    cur = None
    try:
        # Establish connection using the DATABASE_URL loaded from .env
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        yield cur
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        # Log error or handle gracefully in a production app
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            # Rollback any changes just to be safe for a read-only dashboard
            conn.rollback() 
            conn.close()

# --- Data Fetching Functions ---
def fetch_dashboard_data():
    """Fetches movie count and average rating."""
    data = {}
    try:
        with get_db_cursor() as cur:
            # Total Movie Count
            cur.execute("SELECT COUNT(*) FROM movies;")
            data['total_movies'] = cur.fetchone()[0]

            # Average Rating
            cur.execute("SELECT AVG(rating) FROM movies;")
            # Format to a readable string with two decimal places
            avg_rating = cur.fetchone()[0]
            data['avg_rating'] = f"{avg_rating:.2f}" if avg_rating is not None else "N/A"
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        data['total_movies'] = "Error"
        data['avg_rating'] = "Error"
    
    return data

# --- FastAPI Route ---
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Renders the dashboard page with movie statistics."""
    stats = fetch_dashboard_data()
    
    # Context dictionary to pass data to the Jinja2 template
    context = {
        "request": request,
        "title": "Fast Cinema",
        "total_movies": stats['total_movies'],
        "avg_rating": stats['avg_rating']
    }
    
    # Render the template
    return templates.TemplateResponse("dashboard.html", context)

# To run: uvicorn main:app --reload