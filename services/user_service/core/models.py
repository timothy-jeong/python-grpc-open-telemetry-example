import uuid
from sqlalchemy import Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from shared.dao.orm import BaseModel, CreatedAtMixin, UpdatedAtMixin, DeletedAtMixin


class User(BaseModel, CreatedAtMixin, UpdatedAtMixin, DeletedAtMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    nickname: Mapped[str] = mapped_column(Text, unique=False, nullable=False, comment="user nickname")
    email: Mapped[str] = mapped_column(Text, unique=True, nullable=False, comment="user email")
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False, comment="hashed password")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.nickname}', email='{self.email}')>"