"""added email field

Revision ID: 35a20b337d32
Revises: 56a911a20d27
Create Date: 2016-08-09 19:56:07.831053

"""

# revision identifiers, used by Alembic.
revision = '35a20b337d32'
down_revision = '56a911a20d27'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', 'users')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email')
    ### end Alembic commands ###
