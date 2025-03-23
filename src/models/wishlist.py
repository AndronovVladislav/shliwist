from sqlalchemy import ForeignKey, Boolean, text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models.base import Base


class WishlistItem(Base):
    acceptor_id = mapped_column(ForeignKey('users.id'))
    donor_id = mapped_column(ForeignKey('users.id'), nullable=True)

    title: Mapped[int]
    price: Mapped[float]
    link: Mapped[str]
    description: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, server_default=text('true'), nullable=False)

    acceptor = relationship('User', foreign_keys=[acceptor_id], back_populates='wishlist')
    donor = relationship('User', foreign_keys=[donor_id], back_populates='debts')
