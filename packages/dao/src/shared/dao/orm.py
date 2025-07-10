from datetime import UTC, datetime

from sqlalchemy import BigInteger, DateTime, MetaData, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class BaseModel(DeclarativeBase):
    """
    모든 모델이 상속할 Base 클래스.
    Alembic 마이그레이션 시, BaseModel.metadata 를 이용해 테이블 정의를 인식합니다.
    """

    metadata = MetaData(
        naming_convention={
            "all_column_names": lambda constraint, table: "_".join([column.name for column in constraint.columns.values()]),
            "ix": "ix__%(table_name)s__%(all_column_names)s",
            "uq": "uq__%(table_name)s__%(all_column_names)s",
            "ck": "ck__%(table_name)s__%(constraint_name)s",
            "fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
            "pk": "pk__%(table_name)s",
        }
    )


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)
    created_by: Mapped[str] = mapped_column(Text, nullable=False, comment="등록자 정보 경로")

    def create_entity(self,  user_id: str):
        self.created_by = f"users:{user_id}"
        self.deleted_at = datetime.now(UTC)


class UpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[str] = mapped_column(Text, nullable=True, comment="마지막 수정자 정보 경로")

    def update_entity(self, user_id: str):
        self.updated_by = f"users:{user_id}"
        self.updated_at = datetime.now(UTC)


class DeletedAtMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deleted_by: Mapped[str] = mapped_column(Text, nullable=True, comment="마지막 삭제자 정보 경로")

    def delete_entity(self, user_id: str):
        self.deleted_by = f"users:{user_id}"
        self.deleted_at = datetime.now(UTC)