from app.crud.base import CRUDBase
from app.models.portfolio import (
    PortfolioSettings, Project, Skill, Experience, Education, ContactMessage
)
from app.schemas.portfolio import (
    PortfolioSettingsCreate, PortfolioSettingsUpdate,
    ProjectCreate, ProjectUpdate,
    SkillCreate, SkillUpdate,
    ExperienceCreate, ExperienceUpdate,
    EducationCreate, EducationUpdate,
    ContactMessageCreate, ContactMessageUpdate
)

class CRUDPortfolioSettings(CRUDBase[PortfolioSettings, PortfolioSettingsCreate, PortfolioSettingsUpdate]):
    pass

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass

class CRUDSkill(CRUDBase[Skill, SkillCreate, SkillUpdate]):
    pass

class CRUDExperience(CRUDBase[Experience, ExperienceCreate, ExperienceUpdate]):
    pass

class CRUDEducation(CRUDBase[Education, EducationCreate, EducationUpdate]):
    pass

class CRUDContactMessage(CRUDBase[ContactMessage, ContactMessageCreate, ContactMessageUpdate]):
    pass

portfolio_settings = CRUDPortfolioSettings(PortfolioSettings)
project = CRUDProject(Project)
skill = CRUDSkill(Skill)
experience = CRUDExperience(Experience)
education = CRUDEducation(Education)
contact_message = CRUDContactMessage(ContactMessage)
