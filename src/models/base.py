import datetime
import re
from functools import partial
from typing import Annotated

from sqlalchemy import text, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

Id = Annotated[int, mapped_column(primary_key=True)]
NonUpdatableNow = Annotated[
    datetime.datetime,
    mapped_column(server_default=text("TIMEZONE('utc', now())")),
]
UpdatableNow = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=partial(datetime.datetime.now, tz=datetime.UTC),
    ),
]


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_`%(constraint_name)s`',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s'
    })

    id: Mapped[Id]

    repr_cols_num = 5
    repr_cols = tuple()

    def __repr__(self):
        """
        Relationships не используются в repr(), так как могут вести к дополнительным неожиданным запросам.
        """
        cols = []
        for i, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or i < self.repr_cols_num:
                cols.append(f'{col}={getattr(self, col)}')

        return f'<{self.__class__.__name__}: {', '.join(cols)}>'

    def __init_subclass__(cls, **kwargs):
        if '__tablename__' not in cls.__dict__:
            cls.__tablename__ = f'{re.sub(r'(?<!^)(?=[A-Z])', '_', cls.__name__).lower()}s'
        super().__init_subclass__(**kwargs)