"""empty message

Revision ID: d146a6cc0f0b
Revises: 77ce4e5ac20f
Create Date: 2019-12-28 09:19:00.930882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd146a6cc0f0b'
down_revision = '77ce4e5ac20f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follow',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('fid', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uid', 'fid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follow')
    # ### end Alembic commands ###
