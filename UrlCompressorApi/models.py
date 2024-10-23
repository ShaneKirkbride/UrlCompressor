from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create a base class for declarative class definitions
Base = declarative_base()

class URLMapping(Base):
    __tablename__ = 'url_mappings'  # Name of the table in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique identifier
    original_url = Column(String(2048), nullable=False)  # The original long URL
    short_code = Column(String(10), unique=True, nullable=False)  # Generated short code
    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of creation
    expires_at = Column(DateTime, nullable=True)  # Optional expiration timestamp
