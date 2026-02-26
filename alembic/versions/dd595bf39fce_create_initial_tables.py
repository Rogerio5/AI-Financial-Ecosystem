"""Migration script template."""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "dd595bf39fce"
down_revision = "262e1a9dae04"   # baseline anterior
branch_labels = None
depends_on = None

def upgrade() -> None:
    # coloque aqui as operações autogeradas, por exemplo:
    # op.create_table(
    #     'accounts',
    #     sa.Column('id', sa.Integer, primary_key=True),
    #     sa.Column('name', sa.String, nullable=False),
    # )
    pass

def downgrade() -> None:
    # operações para desfazer o upgrade
    pass
