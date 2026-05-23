from __future__ import annotations

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

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
    PortfolioSettingsUpdate,
    PortfolioSkillCreate,
    PortfolioSkillRead,
)


def get_settings(session: Session) -> PortfolioSettings | None:
    return session.scalar(select(PortfolioSettings).order_by(PortfolioSettings.id.asc()).limit(1))


def upsert_settings(session: Session, payload: PortfolioSettingsUpdate) -> PortfolioSettings:
    settings_row = get_settings(session)
    payload_data = payload.model_dump()
    if settings_row is None:
        settings_row = PortfolioSettings(**payload_data)
        session.add(settings_row)
    else:
        for key, value in payload_data.items():
            setattr(settings_row, key, value)
    session.commit()
    session.refresh(settings_row)
    return settings_row


def _ordered_select(model: type) -> Select:
    if hasattr(model, "sort_order"):
        return select(model).order_by(model.sort_order.asc(), model.id.asc())
    return select(model).order_by(model.id.asc())


def list_items(session: Session, model: type) -> list:
    return list(session.scalars(_ordered_select(model)).all())


def get_item(session: Session, model: type, item_id: int):
    return session.get(model, item_id)


def create_item(session: Session, model: type, payload):
    instance = model(**payload.model_dump())
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


def update_item(session: Session, model: type, item_id: int, payload):
    instance = session.get(model, item_id)
    if instance is None:
        return None
    payload_data = payload.model_dump(exclude_unset=True)
    for key, value in payload_data.items():
        setattr(instance, key, value)
    session.commit()
    session.refresh(instance)
    return instance


def delete_item(session: Session, model: type, item_id: int) -> bool:
    instance = session.get(model, item_id)
    if instance is None:
        return False
    session.delete(instance)
    session.commit()
    return True
