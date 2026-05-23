from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class PortfolioSettingsBase(BaseModel):
    owner_name: str = "Your Name"
    title: str = "Software Engineer"
    bio: str = "Building beautiful, scalable, and high-performance applications."
    profile_picture_url: str | None = None
    resume_url: str | None = None
    contact_email: str | None = None


class PortfolioSettingsUpdate(PortfolioSettingsBase):
    pass


class PortfolioSettingsRead(PortfolioSettingsBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioProjectBase(BaseModel):
    title: str
    description: str
    image_url: str | None = None
    is_featured: bool = False
    tech_stack: list[str] = Field(default_factory=list)
    github_url: str | None = None
    live_demo_url: str | None = None
    sort_order: int = 0


class PortfolioProjectCreate(PortfolioProjectBase):
    pass


class PortfolioProjectRead(PortfolioProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioSkillBase(BaseModel):
    name: str
    category: str | None = None
    proficiency_level: int = 0
    sort_order: int = 0


class PortfolioSkillCreate(PortfolioSkillBase):
    pass


class PortfolioSkillRead(PortfolioSkillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioExperienceBase(BaseModel):
    title: str
    company: str
    location: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    sort_order: int = 0


class PortfolioExperienceCreate(PortfolioExperienceBase):
    pass


class PortfolioExperienceRead(PortfolioExperienceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioEducationBase(BaseModel):
    school: str
    degree: str | None = None
    field_of_study: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    description: str | None = None
    sort_order: int = 0


class PortfolioEducationCreate(PortfolioEducationBase):
    pass


class PortfolioEducationRead(PortfolioEducationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
