"""empty message

Revision ID: 8c61621746b0
Revises: 5be6245377a6
Create Date: 2024-03-25 11:52:27.451982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '8c61621746b0'
down_revision: Union[str, None] = '5be6245377a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Post', 'Name',
               existing_type=postgresql.ENUM('OPTION1', 'OPTION2', 'OPTION3', name='nameenum'),
               type_=sa.String(),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Post', 'Name',
               existing_type=sa.String(),
               type_=postgresql.ENUM('OPTION1', 'OPTION2', 'OPTION3', name='nameenum'),
               existing_nullable=False)
    # ### end Alembic commands ###
