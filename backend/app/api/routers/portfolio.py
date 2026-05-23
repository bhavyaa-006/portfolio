import logging
import shutil
from pathlib import Path
from typing import Any, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()
logger = logging.getLogger(__name__)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.get("/settings", response_model=schemas.PortfolioSettings)
def read_portfolio_settings(
    db: Session = Depends(deps.get_db),
) -> Any:
    settings = db.query(models.PortfolioSettings).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Portfolio settings not found")
    return settings

@router.post("/settings", response_model=schemas.PortfolioSettings)
def create_portfolio_settings(
    *,
    db: Session = Depends(deps.get_db),
    settings_in: schemas.PortfolioSettingsCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    settings = db.query(models.PortfolioSettings).first()
    if settings:
        return crud.portfolio_settings.update(db, db_obj=settings, obj_in=settings_in)
    settings = crud.portfolio_settings.create(db, obj_in=settings_in)
    return settings

@router.get("/projects", response_model=List[schemas.Project])
def read_projects(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    projects = crud.project.get_multi(db, skip=skip, limit=limit)
    return projects

@router.post("/projects", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: schemas.ProjectCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    project = crud.project.create(db, obj_in=project_in)
    return project

@router.put("/projects/{id}", response_model=schemas.Project)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    project_in: schemas.ProjectUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    project = crud.project.get(db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project = crud.project.update(db, db_obj=project, obj_in=project_in)
    return project

@router.delete("/projects/{id}", response_model=schemas.Project)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    project = crud.project.get(db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project = crud.project.remove(db, id=id)
    return project

# --- Skills ---
@router.get("/skills", response_model=List[schemas.Skill])
def read_skills(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.skill.get_multi(db, skip=skip, limit=limit)

@router.post("/skills", response_model=schemas.Skill)
def create_skill(*, db: Session = Depends(deps.get_db), item_in: schemas.SkillCreate, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return crud.skill.create(db, obj_in=item_in)

@router.put("/skills/{id}", response_model=schemas.Skill)
def update_skill(*, db: Session = Depends(deps.get_db), id: int, item_in: schemas.SkillUpdate, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    item = crud.skill.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Skill not found")
    return crud.skill.update(db, db_obj=item, obj_in=item_in)

@router.delete("/skills/{id}", response_model=schemas.Skill)
def delete_skill(*, db: Session = Depends(deps.get_db), id: int, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return crud.skill.remove(db, id=id)

# --- Experience ---
@router.get("/experience", response_model=List[schemas.Experience])
def read_experience(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.experience.get_multi(db, skip=skip, limit=limit)

@router.post("/experience", response_model=schemas.Experience)
def create_experience(*, db: Session = Depends(deps.get_db), item_in: schemas.ExperienceCreate, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return crud.experience.create(db, obj_in=item_in)

@router.put("/experience/{id}", response_model=schemas.Experience)
def update_experience(*, db: Session = Depends(deps.get_db), id: int, item_in: schemas.ExperienceUpdate, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    item = crud.experience.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Experience not found")
    return crud.experience.update(db, db_obj=item, obj_in=item_in)

@router.delete("/experience/{id}", response_model=schemas.Experience)
def delete_experience(*, db: Session = Depends(deps.get_db), id: int, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return crud.experience.remove(db, id=id)

# --- Education ---
@router.get("/education", response_model=List[schemas.Education])
def read_education(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100) -> Any:
    return crud.education.get_multi(db, skip=skip, limit=limit)

@router.post("/education", response_model=schemas.Education)
def create_education(*, db: Session = Depends(deps.get_db), item_in: schemas.EducationCreate, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return crud.education.create(db, obj_in=item_in)

@router.put("/education/{id}", response_model=schemas.Education)
def update_education(*, db: Session = Depends(deps.get_db), id: int, item_in: schemas.EducationUpdate, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    item = crud.education.get(db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Education not found")
    return crud.education.update(db, db_obj=item, obj_in=item_in)

@router.delete("/education/{id}", response_model=schemas.Education)
def delete_education(*, db: Session = Depends(deps.get_db), id: int, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return crud.education.remove(db, id=id)

# --- Contact Messages ---
@router.get("/contact", response_model=List[schemas.ContactMessage])
def read_contact_messages(db: Session = Depends(deps.get_db), skip: int = 0, limit: int = 100, current_user: models.User = Depends(deps.get_current_user)) -> Any:
    return crud.contact_message.get_multi(db, skip=skip, limit=limit)

@router.post("/contact", response_model=schemas.ContactMessage)
def create_contact_message(*, db: Session = Depends(deps.get_db), item_in: schemas.ContactMessageCreate) -> Any:
    return crud.contact_message.create(db, obj_in=item_in)

# --- File Uploads ---
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user: models.User = Depends(deps.get_current_user)):
    safe_name = Path(file.filename).name
    file_path = UPLOAD_DIR / safe_name
    logger.info("Uploading file to %s", file_path)
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as exc:
        logger.exception("Upload failed for %s", safe_name)
        raise HTTPException(status_code=500, detail="Failed to upload file") from exc
    return {"url": f"/uploads/{safe_name}"}

