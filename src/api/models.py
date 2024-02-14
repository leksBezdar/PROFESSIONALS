from datetime import datetime
import uuid
from sqlalchemy import ARRAY, JSON, TIMESTAMP, UUID, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class File(Base):
    __tablename__ = 'files'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey('users.id', ondelete='CASCADE'), index=True)
    file_path: Mapped[str] = mapped_column(nullable=False, unique=True)
    file_name: Mapped[str] = mapped_column(nullable=False)
    file_extension: Mapped[str] = mapped_column(nullable=False)
    file_size: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    accessed_users: Mapped[list] = mapped_column(ARRAY(JSON), default=[])
    