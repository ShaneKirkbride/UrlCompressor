
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import Base, URLMapping
from database import engine, get_db
from services import URLShortenerService
from schemas import URLCreateRequest, URLCreateResponse
from starlette.middleware.cors import CORSMiddleware

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()
url_service = URLShortenerService()  # Instantiate the URLShortenerService

# Configure CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins; adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/shorten", response_model=URLCreateResponse)
def create_short_url(request: URLCreateRequest, db: Session = Depends(get_db)):
    """
    Endpoint to create a new short URL.
    """
    # Create a new URL mapping instance
    new_url = URLMapping(
        original_url=request.original_url,
        created_at=datetime.utcnow(),
        expires_at=(
            datetime.utcnow() + timedelta(seconds=request.expiration_time)
        ) if request.expiration_time else None  # Set expiration if provided
    )
    db.add(new_url)  # Add the new URL mapping to the session
    db.commit()  # Commit to save it in the database
    db.refresh(new_url)  # Refresh to get the generated ID

    # Generate the short code using the new URL's ID
    short_code = url_service.encode(new_url.id)
    new_url.short_code = short_code  # Update the URL mapping with the short code
    db.commit()  # Commit the update

    # Construct the full short URL to return
    short_url = f"http://localhost:8000/{short_code}"
    return {"short_url": short_url}  # Return the short URL to the client

@app.get("/{short_code}")
def redirect_to_original(short_code: str, db: Session = Depends(get_db)):
    """
    Endpoint to redirect to the original URL when accessing the short URL.
    """
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
