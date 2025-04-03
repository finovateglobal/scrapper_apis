from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Replace with your actual PostgreSQL connection string.
DATABASE_URL = "demo_link"

# Create the SQLAlchemy engine and sessionmaker for PostgreSQL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the model for your cr_rbi_notifications table with the right column types
class CRRbiNotification(Base):
    __tablename__ = "cr_rbi_notifications"
    
    id = Column(Integer, primary_key=True, index=True)  # Primary key
    guid = Column(Text, nullable=False)                 # GUID column
    title = Column(Text, nullable=False)                # Title column
    link = Column(Text, nullable=False)                 # Link column
    description = Column(Text, nullable=True)           # Description column
    paragraph = Column(Text, nullable=True)             # Paragraph column
    pub_date = Column(DateTime, nullable=True)          # Publication date column

# Optionally create the table if it doesn't exist (for development use only)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to provide a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to read all notifications
@app.get("/notifications/")
def read_notifications(db: Session = Depends(get_db)):
    notifications = db.query(CRRbiNotification).all()
    return notifications

# Endpoint to read a specific notification by its primary key (id)
@app.get("/notifications/{notification_id}")
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    notification = db.query(CRRbiNotification).filter(CRRbiNotification.id == notification_id).first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification
