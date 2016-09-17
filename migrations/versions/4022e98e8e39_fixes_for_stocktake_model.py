"""fixes for stocktake model

Revision ID: 4022e98e8e39
Revises: 319eb76166a
Create Date: 2016-09-07 20:20:45.122380

"""

# revision identifiers, used by Alembic.
revision = '4022e98e8e39'
down_revision = '319eb76166a'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('stocktakes', sa.Column('end_date', sa.DateTime(), nullable=True))
    op.add_column('stocktakes', sa.Column('is_ended', sa.Boolean(), nullable=True))
    op.create_index('ix_stocktakes_end_date', 'stocktakes', ['end_date'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_stocktakes_end_date', 'stocktakes')
    op.drop_column('stocktakes', 'is_ended')
    op.drop_column('stocktakes', 'end_date')
    ### end Alembic commands ###