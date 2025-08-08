"""add summary field to documents

Revision ID: 12748679d72e
Revises: e49b9875d4cb
Create Date: 2025-08-10 00:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "12748679d72e"
down_revision = "e49b9875d4cb"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("summary_html", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "summary_html")
