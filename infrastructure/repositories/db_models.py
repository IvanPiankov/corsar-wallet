from sqlalchemy import DECIMAL, Column, DateTime, ForeignKey, MetaData, String, Table, text
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

accounts = Table(
    "accounts",
    metadata,
    Column("account_id", UUID(as_uuid=True), nullable=False, primary_key=True),
    Column("name", String, nullable=False),
    Column("user_id", UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False),
    Column("account_type", String, nullable=False),
    Column("balance", DECIMAL, nullable=False),
    Column("currency", String, nullable=False),
    Column("created_at", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
    Column("updated_at", DateTime(timezone=True), server_default=text("timezone('utc', now())"), nullable=False),
)

users = Table(
    "users",
    metadata,
    Column("user_id", UUID(as_uuid=True), nullable=False, primary_key=True),
    Column("login", String, nullable=False, unique=True),
    Column("email", String, nullable=False, unique=True),
    Column("hashed_password", String, nullable=False),
    Column("wallet_currency", String, nullable=True),
)
