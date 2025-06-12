"""FastAPI service exposing URL shortening endpoints."""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Base, URLMapping
from database import engine, get_db
from services import URLShortenerService
from schemas import URLCreateRequest, URLCreateResponse
from fastapi.middleware.cors import CORSMiddleware

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()
# Service responsible for Base62 encoding/decoding of IDs
url_service = URLShortenerService()

# Configure CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://10.0.0.185:3000",
    ],  # Specify your frontend origin
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],  # Explicitly include POST and OPTIONS methods
    allow_headers=["*"],
)


@app.post("/shorten", response_model=URLCreateResponse)
def create_short_url(
    request: URLCreateRequest, request_obj: Request, db: Session = Depends(get_db)
):
    """Create a new short URL and return the generated link."""
    # Convert the URL to a string before storing
    original_url_str = str(request.original_url)
    # Temporary code used so the record can be flushed and an ID generated
    temp_code = f"tmp_{datetime.utcnow().timestamp()}"

    # Calculate the expiration time
    expires_at = (
        (datetime.utcnow() + timedelta(seconds=request.expiration_time))
        if request.expiration_time
        else None
    )

    # Create a new URL mapping instance without 'short_code'
    new_url = URLMapping(
        original_url=original_url_str,
        short_code=temp_code,
        created_at=datetime.utcnow(),
        expires_at=expires_at,
    )

    db.add(new_url)
    db.flush()  # Flush so new_url.id is populated without a full commit

    if new_url.id is None:
        raise HTTPException(
            status_code=500, detail="Failed to generate short URL. Please try again."
        )

    # Generate the short code using the new URL's ID
    short_code = url_service.encode(new_url.id)
    new_url.short_code = short_code  # Update the URL mapping with the short code

    # Now commit the transaction
    db.commit()
    db.refresh(new_url)  # Refresh to get the latest data from the database

    # Construct the full short URL to return using request_obj
    short_url = f"{request_obj.base_url}{short_code}"
    return {"short_url": short_url}  # Return the short URL to the client


@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    """Lookup the short code and redirect the client to the original URL."""
    try:
        # Decode the short code to get the original ID
        entry_id = url_service.decode(short_code)
    except ValueError:
        # If decoding fails, the URL is invalid
        raise HTTPException(status_code=404, detail="Invalid URL")

    # Retrieve the URL mapping from the database
    url_mapping = db.query(URLMapping).filter(URLMapping.id == entry_id).first()

    if url_mapping is None:
        # No mapping found for the given ID
        raise HTTPException(status_code=404, detail="URL not found")

    if url_mapping.expires_at and datetime.utcnow() > url_mapping.expires_at:
        # The URL has expired
        raise HTTPException(status_code=410, detail="URL has expired")

    # Redirect to the original URL
    return RedirectResponse(url=url_mapping.original_url)
