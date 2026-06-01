"""add upstream proxy routing

Revision ID: 20260601_010000_add_upstream_proxy_routing
Revises: 20260601_000000_merge_relative_availability_and_usage_raw_heads
Create Date: 2026-06-01 15:10:00.000000
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "20260601_010000_add_upstream_proxy_routing"
down_revision = "20260601_000000_merge_relative_availability_and_usage_raw_heads"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "proxy_endpoints",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("scheme", sa.String(), nullable=False),
        sa.Column("host", sa.String(), nullable=False),
        sa.Column("port", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=True),
        sa.Column("password_encrypted", sa.LargeBinary(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "proxy_pools",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "proxy_pool_members",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("pool_id", sa.String(), nullable=False),
        sa.Column("endpoint_id", sa.String(), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("weight", sa.Integer(), server_default=sa.text("1"), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["endpoint_id"], ["proxy_endpoints.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pool_id"], ["proxy_pools.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("pool_id", "endpoint_id", name="uq_proxy_pool_members_pool_endpoint"),
    )
    op.create_index(
        "idx_proxy_pool_members_pool_order",
        "proxy_pool_members",
        ["pool_id", "is_active", "sort_order", "id"],
    )
    op.create_table(
        "account_proxy_bindings",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("account_id", sa.String(), nullable=False),
        sa.Column("pool_id", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["pool_id"], ["proxy_pools.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("account_id", name="uq_account_proxy_bindings_account"),
    )
    with op.batch_alter_table("dashboard_settings") as batch_op:
        batch_op.add_column(
            sa.Column("upstream_proxy_routing_enabled", sa.Boolean(), server_default=sa.false(), nullable=False)
        )
        batch_op.add_column(sa.Column("upstream_proxy_default_pool_id", sa.String(), nullable=True))
        batch_op.create_foreign_key(
            "fk_dashboard_settings_upstream_proxy_default_pool",
            "proxy_pools",
            ["upstream_proxy_default_pool_id"],
            ["id"],
            ondelete="SET NULL",
        )
    op.add_column("request_logs", sa.Column("upstream_proxy_route_mode", sa.String(), nullable=True))
    op.add_column("request_logs", sa.Column("upstream_proxy_pool_id", sa.String(), nullable=True))
    op.add_column("request_logs", sa.Column("upstream_proxy_endpoint_id", sa.String(), nullable=True))
    op.add_column("request_logs", sa.Column("upstream_proxy_fallback_used", sa.Boolean(), nullable=True))
    op.add_column("request_logs", sa.Column("upstream_proxy_fail_closed_reason", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("request_logs", "upstream_proxy_fail_closed_reason")
    op.drop_column("request_logs", "upstream_proxy_fallback_used")
    op.drop_column("request_logs", "upstream_proxy_endpoint_id")
    op.drop_column("request_logs", "upstream_proxy_pool_id")
    op.drop_column("request_logs", "upstream_proxy_route_mode")
    with op.batch_alter_table("dashboard_settings") as batch_op:
        batch_op.drop_constraint("fk_dashboard_settings_upstream_proxy_default_pool", type_="foreignkey")
        batch_op.drop_column("upstream_proxy_default_pool_id")
        batch_op.drop_column("upstream_proxy_routing_enabled")
    op.drop_table("account_proxy_bindings")
    op.drop_index("idx_proxy_pool_members_pool_order", table_name="proxy_pool_members")
    op.drop_table("proxy_pool_members")
    op.drop_table("proxy_pools")
    op.drop_table("proxy_endpoints")
