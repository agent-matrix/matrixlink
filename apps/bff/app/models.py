from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime
from datetime import datetime
import uuid
from .db import Base

def _uuid() -> str: return str(uuid.uuid4())

class Agent(Base):
    __tablename__ = "agents"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    name: Mapped[str] = mapped_column(String(120), index=True)
    type: Mapped[str] = mapped_column(String(20), default="app")
    image: Mapped[str] = mapped_column(String(512), default="")
    catalog_url: Mapped[str] = mapped_column(Text, default="")
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

class Run(Base):
    __tablename__ = "runs"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    agent_id: Mapped[str] = mapped_column(String(36), index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), default="default", index=True)
    status: Mapped[str] = mapped_column(String(20), default="queued", index=True)
    request_json: Mapped[str] = mapped_column(Text, default="{}")
    result_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, default=None)
