"""merge heads 1e6fad8041aa and dd595bf39fce"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'merge_1e6f_dd59'
down_revision = ('1e6fad8041aa', 'dd595bf39fce')
branch_labels = None
depends_on = None

def upgrade():
    # no-op: registra a união das linhas de migração
    pass

def downgrade():
    # no-op
    pass
