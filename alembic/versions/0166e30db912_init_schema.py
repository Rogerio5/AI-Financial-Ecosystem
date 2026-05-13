"""init schema"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "init_schema"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("cpf", sa.String(length=11), primary_key=True, index=True),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=True),
    )

    op.create_table(
        "accounts",
        sa.Column("id", sa.String(length=20), primary_key=True, index=True),
        sa.Column("owner_cpf", sa.String(length=11), sa.ForeignKey("customers.cpf"), nullable=False),
        sa.Column("balance", sa.Float, nullable=False, server_default="0.0"),
    )

    op.create_table(
        "transactions",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("account_id", sa.String(length=20), sa.ForeignKey("accounts.id"), nullable=False, index=True),
        sa.Column("date", sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column("type", sa.String(length=20)),
        sa.Column("amount", sa.Float),
        sa.Column("balance_after", sa.Float),
        sa.Column("description", sa.Text),
    )

def downgrade() -> None:
    op.drop_table("transactions")
    op.drop_table("accounts")
    op.drop_table("customers")
