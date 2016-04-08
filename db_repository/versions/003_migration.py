from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
fimposto = Table('fimposto', pre_meta,
    Column('faturas_id', INTEGER, primary_key=True, nullable=False),
    Column('imposto_id', INTEGER, primary_key=True, nullable=False),
    Column('aliquota', FLOAT),
    Column('deducao', FLOAT),
    Column('v_faturamento', FLOAT),
    Column('date_created', DATETIME),
    Column('date_modified', DATETIME),
)

imposto = Table('imposto', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('descricao', VARCHAR(length=100)),
    Column('date_created', DATETIME),
    Column('date_modified', DATETIME),
)

imposto = Table('imposto', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('valor_faturamento', Float),
    Column('pis_aliquota', Float),
    Column('pis_deducao', Float),
    Column('cofins_aliquota', Float),
    Column('cofins_deducao', Float),
    Column('csll_aliquota', Float),
    Column('csll_deducao', Float),
    Column('irpj_aliquota', Float),
    Column('irpj_deducao', Float),
    Column('iss_aliquota', Float),
    Column('iss_deducao', Float),
    Column('faturas_id', Integer),
    Column('date_created', DateTime),
    Column('date_modified', DateTime),
)

reembolso = Table('reembolso', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('descricao', VARCHAR(length=100)),
    Column('valor', FLOAT),
    Column('cliente_id', INTEGER),
    Column('faturamento_id', INTEGER),
    Column('date_created', DATETIME),
    Column('date_modified', DATETIME),
)

reembolso = Table('reembolso', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('descricao', String(length=100)),
    Column('valor', Float),
    Column('date_created', DateTime),
    Column('date_modified', DateTime),
    Column('faturas_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['fimposto'].drop()
    pre_meta.tables['imposto'].columns['descricao'].drop()
    post_meta.tables['imposto'].columns['cofins_aliquota'].create()
    post_meta.tables['imposto'].columns['cofins_deducao'].create()
    post_meta.tables['imposto'].columns['csll_aliquota'].create()
    post_meta.tables['imposto'].columns['csll_deducao'].create()
    post_meta.tables['imposto'].columns['faturas_id'].create()
    post_meta.tables['imposto'].columns['irpj_aliquota'].create()
    post_meta.tables['imposto'].columns['irpj_deducao'].create()
    post_meta.tables['imposto'].columns['iss_aliquota'].create()
    post_meta.tables['imposto'].columns['iss_deducao'].create()
    post_meta.tables['imposto'].columns['pis_aliquota'].create()
    post_meta.tables['imposto'].columns['pis_deducao'].create()
    post_meta.tables['imposto'].columns['valor_faturamento'].create()
    pre_meta.tables['reembolso'].columns['cliente_id'].drop()
    pre_meta.tables['reembolso'].columns['faturamento_id'].drop()
    post_meta.tables['reembolso'].columns['faturas_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['fimposto'].create()
    pre_meta.tables['imposto'].columns['descricao'].create()
    post_meta.tables['imposto'].columns['cofins_aliquota'].drop()
    post_meta.tables['imposto'].columns['cofins_deducao'].drop()
    post_meta.tables['imposto'].columns['csll_aliquota'].drop()
    post_meta.tables['imposto'].columns['csll_deducao'].drop()
    post_meta.tables['imposto'].columns['faturas_id'].drop()
    post_meta.tables['imposto'].columns['irpj_aliquota'].drop()
    post_meta.tables['imposto'].columns['irpj_deducao'].drop()
    post_meta.tables['imposto'].columns['iss_aliquota'].drop()
    post_meta.tables['imposto'].columns['iss_deducao'].drop()
    post_meta.tables['imposto'].columns['pis_aliquota'].drop()
    post_meta.tables['imposto'].columns['pis_deducao'].drop()
    post_meta.tables['imposto'].columns['valor_faturamento'].drop()
    pre_meta.tables['reembolso'].columns['cliente_id'].create()
    pre_meta.tables['reembolso'].columns['faturamento_id'].create()
    post_meta.tables['reembolso'].columns['faturas_id'].drop()
