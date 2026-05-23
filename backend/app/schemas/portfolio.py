from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

# --- PortfolioSettings ---
class PortfolioSettingsBase(BaseModel):
    owner_name: str
    title: Optional[str] = None
    bio: Optional[str] = None
    resume_url: Optional[str] = None
    profile_picture_url: Optional[str] = None
    contact_email: Optional[str] = None

class PortfolioSettingsCreate(PortfolioSettingsBase):
    pass

class PortfolioSettingsUpdate(PortfolioSettingsBase):
    owner_name: Optional[str] = None

class PortfolioSettings(PortfolioSettingsBase):
    id: int
    class Config:
        from_attributes = True

# --- Project ---
class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    tech_stack: Optional[List[str]] = []
    github_url: Optional[str] = None
    live_demo_url: Optional[str] = None
    is_featured: Optional[bool] = False
    order: Optional[int] = 0

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    title: Optional[str] = None

class Project(ProjectBase):
    id: int
    class Config:
        from_attributes = True

# --- Skill ---
class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None
    icon: Optional[str] = None
    proficiency: Optional[int] = None
    order: Optional[int] = 0

class SkillCreate(SkillBase):
    pass

class SkillUpdate(SkillBase):
    name: Optional[str] = None

class Skill(SkillBase):
    id: int
    class Config:
        from_attributes = True

# --- Experience ---
class ExperienceBase(BaseModel):
    company: str
    role: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    is_current: Optional[bool] = False
    order: Optional[int] = 0

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceUpdate(ExperienceBase):
    company: Optional[str] = None
    role: Optional[str] = None

class Experience(ExperienceBase):
    id: int
    class Config:
        from_attributes = True

# --- Education ---
class EducationBase(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = 0

class EducationCreate(EducationBase):
    pass

class EducationUpdate(EducationBase):
    institution: Optional[str] = None
    degree: Optional[str] = None

class Education(EducationBase):
    id: int
    class Config:
        from_attributes = True

# --- ContactMessage ---
class ContactMessageBase(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessageUpdate(ContactMessageBase):
    is_read: Optional[bool] = None

class ContactMessage(ContactMessageBase):
    id: int
    created_at: datetime
    is_read: bool
    class Config:
        from_attributes = True
