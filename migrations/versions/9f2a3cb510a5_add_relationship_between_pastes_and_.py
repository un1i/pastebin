"""Add relationship between pastes and users

Revision ID: 9f2a3cb510a5
Revises: 57817e93e6f5
Create Date: 2023-08-11 16:34:47.804375

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f2a3cb510a5'
down_revision = '57817e93e6f5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('paste', sa.Column('author_id', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'paste', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'paste', type_='foreignkey')
    op.drop_column('paste', 'author_id')
    # ### end Alembic commands ###