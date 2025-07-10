from typing import Any
from sqlalchemy.orm import Session
from .model import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        """사용자 ID로 사용자를 조회합니다."""
        return self.db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()

    def create(self, username: str, email: str, hashed_password: str, creator_id: str) -> User:
        """새로운 사용자를 생성합니다."""
        db_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
        )
        db_user.create_entity(user_id=creator_id)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, updater_id: str, data: dict[str, Any]) -> User | None:
        """사용자 정보를 수정합니다."""
        db_user = self.get_by_id(user_id)
        if db_user:
            for key, value in data.items():
                setattr(db_user, key, value)
            db_user.update_entity(user_id=updater_id)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete(self, user_id: int, deleter_id: str) -> User | None:
        """사용자 정보를 삭제 처리(soft delete)합니다."""
        db_user = self.get_by_id(user_id)
        if db_user:
            db_user.delete_entity(user_id=deleter_id)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user 