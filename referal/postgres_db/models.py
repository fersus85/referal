from uuid import UUID, uuid4
from typing import Optional, List

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from referal.core.db import Base
from referal.postgres_db.schemas import ReferalCode


class User_referer(Base):
    __tablename__ = 'user_referer'
    __table_args__ = UniqueConstraint('email')

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    email: Mapped[str]
    hashed_password: Mapped[str]
    referal_code: Mapped[Optional[ReferalCode]]

    referals: Mapped[List['UserReferal']] = relationship(
        back_populates='referer')


class UserReferal(Base):
    __tablename__ = 'user_referal'
    __table_args__ = UniqueConstraint('email')

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    referer_id: Mapped[UUID] = mapped_column(ForeignKey('user_referer.id'))
    email: Mapped[str]
    hashed_password: Mapped[str]

    referer: Mapped[User_referer] = relationship(back_populates='referal')
