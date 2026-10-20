"""Create workout tables

Revision ID: 217bde5e2b3d
Revises: d37bc03abf6c
Create Date: 2026-10-20 12:57:19.031055

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '217bde5e2b3d'
down_revision = 'd37bc03abf6c'
branch_labels = None
depends_on = None


def upgrade():
    # The previous migration already creates all workout tables.
    # No additional schema changes are needed in this revision.
    pass

def downgrade():
    # The previous migration is responsible for droping the tables.
    pass
