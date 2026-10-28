"""Create QSR application-owned tables additively."""
from alembic import op
from app.db.base import Base
from app import models  # noqa: F401
revision = "0001_qsr_tables"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Creates declared qsr_* tables only when absent; no legacy tables are dropped.
    Base.metadata.create_all(bind=op.get_bind(), checkfirst=True)

def downgrade():
    # Intentionally non-destructive. Approve a retention plan before any rollback deletes data.
    pass
