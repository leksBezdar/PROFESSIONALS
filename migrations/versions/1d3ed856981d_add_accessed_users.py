"""add accessed users

Revision ID: 1d3ed856981d
Revises: 981d7a769e32
Create Date: 2024-02-03 20:45:06.889984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d3ed856981d'
down_revision: Union[str, None] = '981d7a769e32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('accessed_users', sa.ARRAY(sa.JSON()), nullable=False, server_default='{}'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('files', 'accessed_users')
    # ### end Alembic commands ###
