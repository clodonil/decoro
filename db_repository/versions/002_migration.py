from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Faturas_Imposto = Table('Faturas_Imposto', pre_meta,
    Column('faturas_id', INTEGER, primary_key=True, nullable=False),
    Column('imposto_id', INTEGER, primary_key=True, nullable=False),
    Column('aliquota', FLOAT),
    Column('valor', FLOAT),
    Column('faturamento', FLOAT),
)

fimposto = Table('fimposto', post_meta,
    Column('faturas_id', Integer, primary_key=True, nullable=False),
    Column('imposto_id', Integer, primary_key=True, nullable=False),
    Column('aliquota', Float),
    Column('deducao', Float),
    Column('v_faturamento', Float),
    Column('date_created', DateTime),
    Column('date_modified', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Faturas_Imposto'].drop()
    post_meta.tables['fimposto'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Faturas_Imposto'].create()
    post_meta.tables['fimposto'].drop()
