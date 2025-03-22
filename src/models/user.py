from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base, NonUpdatableNow, Id


class User(Base):
    username: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str]

    profile: Mapped['Profile'] = relationship(back_populates='user')

    wishlist: Mapped[list['WishlistItem']] = relationship('WishlistItem',
                                                          foreign_keys='WishlistItem.acceptor_id',
                                                          back_populates='acceptor',
                                                          )
    debts: Mapped[list['WishlistItem']] = relationship('WishlistItem',
                                                       foreign_keys='WishlistItem.donor_id',
                                                       back_populates='donor',
                                                       )


class Profile(Base):
    name: Mapped[str]
    surname: Mapped[str]
    registered_at: Mapped[NonUpdatableNow]

    user_id: Mapped[Id] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='profile')
