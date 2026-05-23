from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class PortfolioSettings(Base):
    __tablename__ = "portfolio_settings"
    id = Column(Integer, primary_key=True, index=True)
    owner_name = Column(String, nullable=False)
    title = Column(String)
    bio = Column(String)
    resume_url = Column(String)
    profile_picture_url = Column(String)
    contact_email = Column(String)

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    image_url = Column(String)
    tech_stack = Column(JSON) # Store list of strings
    github_url = Column(String)
    live_demo_url = Column(String)
    is_featured = Column(Boolean, default=False)
    order = Column(Integer, default=0)

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String) # e.g. Frontend, Backend, Tools
    icon = Column(String)
    proficiency = Column(Integer) # 0-100
    order = Column(Integer, default=0)

class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    role = Column(String, nullable=False)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(String)
    is_current = Column(Boolean, default=False)
    order = Column(Integer, default=0)

class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, index=True)
    institution = Column(String, nullable=False)
    degree = Column(String, nullable=False)
    field_of_study = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(String)
    order = Column(Integer, default=0)

class ContactMessage(Base):
    __tablename__ = "contact_messages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    subject = Column(String)
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_read = Column(Boolean, default=False)
