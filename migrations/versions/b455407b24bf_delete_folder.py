"""Delete folder

Revision ID: b455407b24bf
Revises: 1d3ed856981d
Create Date: 2024-02-06 21:19:12.457007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b455407b24bf'
down_revision: Union[str, None] = '1d3ed856981d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_folders_id', table_name='folders')
    op.drop_constraint('files_folder_id_fkey', 'files', type_='foreignkey')
    op.drop_table('folders')
    op.drop_column('files', 'folder_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('folder_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('files_folder_id_fkey', 'files', 'folders', ['folder_id'], ['id'], ondelete='CASCADE')
    op.create_table('folders',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('folder_name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('folder_path', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('parent_folder_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['parent_folder_id'], ['folders.id'], name='folders_parent_folder_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='folders_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='folders_pkey'),
    sa.UniqueConstraint('folder_path', name='folders_folder_path_key')
    )
    op.create_index('ix_folders_id', 'folders', ['id'], unique=False)
    # ### end Alembic commands ###