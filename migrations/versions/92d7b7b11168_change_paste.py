"""change paste

Revision ID: 92d7b7b11168
Revises: dfc13e65aa5d
Create Date: 2023-07-12 21:06:17.270535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92d7b7b11168'
down_revision = 'dfc13e65aa5d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('paste',
    sa.Column('id', sa.VARCHAR(length=8), nullable=False),
    sa.Column('url', sa.TEXT(), nullable=False),
    sa.Column('date_creation', sa.TIMESTAMP(), nullable=False),
    sa.Column('date_delete', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('paste')
    # ### end Alembic commands ###