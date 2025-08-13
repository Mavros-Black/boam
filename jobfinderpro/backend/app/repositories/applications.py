from __future__ import annotations
from typing import Optional
from sqlalchemy.orm import Session
from app.models import Application


def create_application(session: Session, application: Application) -> Application:
    session.add(application)
    session.commit()
    session.refresh(application)
    return application


def get_application(session: Session, app_id: int) -> Optional[Application]:
    return session.get(Application, app_id)


def update_application_success(session: Session, app_id: int, success: bool) -> Optional[Application]:
    application = session.get(Application, app_id)
    if not application:
        return None
    application.success = success
    session.commit()
    session.refresh(application)
    return application