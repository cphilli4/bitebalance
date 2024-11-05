"""create meal table

Revision ID: f3324141b0ff
Revises: 
Create Date: 2024-10-27 18:38:25.943559

"""
import logging
from logging.config import fileConfig
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.global_config import app_config 


# revision identifiers, used by Alembic.
revision: str = 'f3324141b0ff'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Interpret the config file for logging
logger = logging.getLogger("alembic.env")

# Add this line before creating any tables that use uuid_generate_v4()
op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")


def upgrade() -> None:
    logger.info("Running UPGRADE")
    op.create_table(
        "meals",
        sa.Column("id",
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),),
        sa.Column("label", sa.VARCHAR, nullable=False, index=True),
        sa.Column("url", sa.VARCHAR, nullable=True),
        sa.Column("meal_data", JSONB, nullable=True),
        sa.Column("created_at", sa.TIMESTAMP, nullable=True, server_default=sa.text("now()")),
        sa.Column("updated_at", sa.TIMESTAMP, nullable=True),
        sa.Column("deleted_at", sa.TIMESTAMP, nullable=True),
    )


def downgrade() -> None:
    logger.info("Running UPGRADE")
    op.drop_table("meals")
