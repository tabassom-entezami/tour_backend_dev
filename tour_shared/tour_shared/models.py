import uuid

from sqlalchemy import DateTime, Column, TypeDecorator, CHAR, MetaData
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from tour_shared.utils import now

meta = MetaData(naming_convention={
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
})


class UUIDField(TypeDecorator):
    impl = UUID
    cache_ok = True

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('as_uuid', True)
        super().__init__(*args, **kwargs)


class ModificationTimeMixing:
    created_at = Column(
        DateTime(timezone=True),
        default=now,
        nullable=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=now,
        onupdate=now,
        nullable=True
    )
    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True
    )


def uuid_pk_column():
    return Column(
        'id',
        UUIDField,
        primary_key=True,
        nullable=False,
        default=lambda: uuid.uuid4()
    )


def temporal_columns():
    return (
        Column(
            'created_at',
            DateTime(timezone=True),
            default=now,
            nullable=True
        ),
        Column(
            'updated_at',
            DateTime(timezone=True),
            default=now,
            onupdate=now,
            nullable=True
        ),
        Column(
            'deleted_at',
            DateTime(timezone=True),
            nullable=True
        )
    )


class Base(object):
    id = Column(UUIDField,
                primary_key=True,
                nullable=False,
                default=lambda: uuid.uuid4().hex)


DeclarativeBase = declarative_base(cls=Base, metadata=meta)
EmptyDeclarativeBase = declarative_base(metadata=meta)
