from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.portfolio import (
    PortfolioEducation,
    PortfolioExperience,
    PortfolioProject,
    PortfolioSettings,
    PortfolioSkill,
)
from app.schemas.portfolio import (
    PortfolioEducationCreate,
    PortfolioEducationRead,
    PortfolioExperienceCreate,
    PortfolioExperienceRead,
    PortfolioProjectCreate,
    PortfolioProjectRead,
    PortfolioSettingsRead,
    PortfolioSettingsUpdate,
    PortfolioSkillCreate,
    PortfolioSkillRead,
)
from app.services.portfolio_service import (
    create_item,
    delete_item,
    get_item,
    get_settings,
    list_items,
    upsert_settings,
    update_item,
)
from app.utils.dependencies import get_current_superuser

router = APIRouter(prefix="/portfolio", tags=["portfolio"])
admin_router = APIRouter(
    prefix="/admin/portfolio",
    tags=["portfolio-admin"],
    dependencies=[Depends(get_current_superuser)],
)


@router.get("/settings", response_model=PortfolioSettingsRead | None)
def read_public_settings(session: Session = Depends(get_db)):
    return get_settings(session)


@router.get("/projects", response_model=list[PortfolioProjectRead])
def read_public_projects(session: Session = Depends(get_db)):
    return list_items(session, PortfolioProject)


@router.get("/skills", response_model=list[PortfolioSkillRead])
def read_public_skills(session: Session = Depends(get_db)):
    return list_items(session, PortfolioSkill)


@router.get("/experience", response_model=list[PortfolioExperienceRead])
def read_public_experience(session: Session = Depends(get_db)):
    return list_items(session, PortfolioExperience)


@router.get("/education", response_model=list[PortfolioEducationRead])
def read_public_education(session: Session = Depends(get_db)):
    return list_items(session, PortfolioEducation)


@admin_router.put("/settings", response_model=PortfolioSettingsRead)
def upsert_public_settings(payload: PortfolioSettingsUpdate, session: Session = Depends(get_db)):
    return upsert_settings(session, payload)


@admin_router.get("/projects", response_model=list[PortfolioProjectRead])
def admin_list_projects(session: Session = Depends(get_db)):
    return list_items(session, PortfolioProject)


@admin_router.post("/projects", response_model=PortfolioProjectRead, status_code=status.HTTP_201_CREATED)
def admin_create_project(payload: PortfolioProjectCreate, session: Session = Depends(get_db)):
    return create_item(session, PortfolioProject, payload)


@admin_router.put("/projects/{project_id}", response_model=PortfolioProjectRead)
def admin_update_project(project_id: int, payload: PortfolioProjectCreate, session: Session = Depends(get_db)):
    project = update_item(session, PortfolioProject, project_id, payload)
    if project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@admin_router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_project(project_id: int, session: Session = Depends(get_db)):
    if not delete_item(session, PortfolioProject, project_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@admin_router.get("/skills", response_model=list[PortfolioSkillRead])
def admin_list_skills(session: Session = Depends(get_db)):
    return list_items(session, PortfolioSkill)


@admin_router.post("/skills", response_model=PortfolioSkillRead, status_code=status.HTTP_201_CREATED)
def admin_create_skill(payload: PortfolioSkillCreate, session: Session = Depends(get_db)):
    return create_item(session, PortfolioSkill, payload)


@admin_router.put("/skills/{skill_id}", response_model=PortfolioSkillRead)
def admin_update_skill(skill_id: int, payload: PortfolioSkillCreate, session: Session = Depends(get_db)):
    skill = update_item(session, PortfolioSkill, skill_id, payload)
    if skill is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return skill


@admin_router.delete("/skills/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_skill(skill_id: int, session: Session = Depends(get_db)):
    if not delete_item(session, PortfolioSkill, skill_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@admin_router.get("/experience", response_model=list[PortfolioExperienceRead])
def admin_list_experience(session: Session = Depends(get_db)):
    return list_items(session, PortfolioExperience)


@admin_router.post("/experience", response_model=PortfolioExperienceRead, status_code=status.HTTP_201_CREATED)
def admin_create_experience(payload: PortfolioExperienceCreate, session: Session = Depends(get_db)):
    return create_item(session, PortfolioExperience, payload)


@admin_router.put("/experience/{experience_id}", response_model=PortfolioExperienceRead)
def admin_update_experience(experience_id: int, payload: PortfolioExperienceCreate, session: Session = Depends(get_db)):
    experience = update_item(session, PortfolioExperience, experience_id, payload)
    if experience is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    return experience


@admin_router.delete("/experience/{experience_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_experience(experience_id: int, session: Session = Depends(get_db)):
    if not delete_item(session, PortfolioExperience, experience_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@admin_router.get("/education", response_model=list[PortfolioEducationRead])
def admin_list_education(session: Session = Depends(get_db)):
    return list_items(session, PortfolioEducation)


@admin_router.post("/education", response_model=PortfolioEducationRead, status_code=status.HTTP_201_CREATED)
def admin_create_education(payload: PortfolioEducationCreate, session: Session = Depends(get_db)):
    return create_item(session, PortfolioEducation, payload)


@admin_router.put("/education/{education_id}", response_model=PortfolioEducationRead)
def admin_update_education(education_id: int, payload: PortfolioEducationCreate, session: Session = Depends(get_db)):
    education = update_item(session, PortfolioEducation, education_id, payload)
    if education is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")
    return education


@admin_router.delete("/education/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_education(education_id: int, session: Session = Depends(get_db)):
    if not delete_item(session, PortfolioEducation, education_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Education not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
